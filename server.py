#!/usr/bin/env python3
"""Flask web interface for the Whiteout Survival Gift Code Redeemer."""

import os
import sys
import subprocess
import tempfile
import threading
import queue
import time
from flask import Flask, render_template, request, Response, jsonify, stream_with_context

app = Flask(__name__)

# Track active jobs
active_jobs = {}
job_lock = threading.Lock()

def run_redemption(job_id, code, fids_content, ocr_method, save_images):
    """Run the redemption script and stream output."""
    q = active_jobs[job_id]["queue"]
    
    try:
        # Write FIDs to a temp CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, dir='/tmp') as f:
            f.write(fids_content)
            csv_path = f.name

        cmd = [
            sys.executable, "redeem_codes.py",
            "--code", code,
            "--csv", csv_path,
            "--ocr-method", ocr_method,
            "--save-images", str(save_images)
        ]

        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        with job_lock:
            active_jobs[job_id]["pid"] = proc.pid

        for line in iter(proc.stdout.readline, ''):
            q.put({"type": "line", "text": line.rstrip()})

        proc.stdout.close()
        proc.wait()

        if proc.returncode == 0:
            q.put({"type": "done", "text": "Redemption complete."})
        else:
            q.put({"type": "error", "text": f"Process exited with code {proc.returncode}."})

    except Exception as e:
        q.put({"type": "error", "text": f"Server error: {e}"})
    finally:
        try:
            os.unlink(csv_path)
        except Exception:
            pass
        with job_lock:
            active_jobs[job_id]["running"] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    code = request.form.get("code", "").strip()
    fids_raw = request.form.get("fids", "").strip()
    ocr_method = request.form.get("ocr_method", "onnx")
    save_images = request.form.get("save_images", "0")

    # Handle uploaded CSV file
    uploaded = request.files.get("csv_file")
    if uploaded and uploaded.filename:
        fids_raw = uploaded.read().decode("utf-8", errors="replace").strip()

    if not code:
        return jsonify({"error": "Gift code is required."}), 400
    if not fids_raw:
        return jsonify({"error": "Player IDs are required."}), 400

    job_id = str(int(time.time() * 1000))
    q = queue.Queue()

    with job_lock:
        active_jobs[job_id] = {"queue": q, "running": True, "pid": None}

    thread = threading.Thread(
        target=run_redemption,
        args=(job_id, code, fids_raw, ocr_method, save_images),
        daemon=True
    )
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/stream/<job_id>")
def stream(job_id):
    def generate():
        if job_id not in active_jobs:
            yield "data: {\"type\": \"error\", \"text\": \"Job not found.\"}\n\n"
            return

        job = active_jobs[job_id]
        q = job["queue"]

        while True:
            try:
                msg = q.get(timeout=0.5)
                import json
                yield f"data: {json.dumps(msg)}\n\n"
                if msg["type"] in ("done", "error"):
                    break
            except queue.Empty:
                if not job.get("running", False):
                    break
                yield "data: {\"type\": \"ping\"}\n\n"

        with job_lock:
            active_jobs.pop(job_id, None)

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
