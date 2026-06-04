# Whiteout Survival Gift Code Redemption Script

Python script that automates the process of redeeming gift codes in the game **Whiteout Survival**. It reads a list of Player IDs from one or more `.csv` files, automatically solves the CAPTCHA required by the API using a custom-trained ONNX model (or a fallback OCR method), sends requests to the game's giftcode redemption API, and redeems the specified gift code for each player.

It was built with the goal of providing an alternative to [the Discord Bot](https://github.com/whiteout-project/bot) that I'm also helping develop. Setting up the bot and hosting it can take some effort to do, while this script can be run with one simple command. It can also be seen as providing a kind of backup option when your Discord bot is down and redemption is failing. The bot is awesome though - check it out if you haven't already.

---

## Prerequisites

1.  **Python 3.9+**: Download and install Python 3.9 or later from [python.org](https://www.python.org/). Ensure Python is added to your system's PATH during installation.
2.  **Core Libraries**: Install the base libraries required by the script:
    ```bash
    pip install requests numpy pillow colorama
    ```
3.  **OCR Libraries**: Install **at least one** of the following based on the `--ocr-method` you intend to use:
    *   **For `onnx` (Recommended Default, ~98% Success Rate, Lightweight):**
        ```bash
        pip install onnxruntime
        ```
        *(Uses a custom-trained ONNX model included in the `model/` directory. No additional model downloads needed.)*

    *   **For `ddddocr` (~80% Success Rate, Lightweight):**
        ```bash
        pip install ddddocr==1.5.6 opencv-python --ignore-requires-python
        ```
        *(Note: --ignore-requires-python is required to support Python 3.13 and beyond. Requires `opencv-python`.)*

    *   **For `easyocr` (~40-50% Success Rate, Heavy Requirements):**
        ```bash
        pip install easyocr torch torchvision torchaudio opencv-python
        ```
        *(Note: `torch` install might vary based on your system/CUDA version if using GPU. See GPU section below. This installs PyTorch for CPU. Requires `opencv-python`.)*

    *   **For `captchacracker` (~40-50% Success Rate, Moderate Requirements):**
        ```bash
        pip install captchacracker opencv-python
        ```
        *(Note: This will install `tensorflow`. You also need the `model/weights.h5` file placed correctly relative to the script. Requires `opencv-python`.)*

---

## Setup

1.  **Get the Script**:
    *   Clone the repository: `git clone https://github.com/justncodes/wos-giftcode.git`
    *   The `model/` directory contains the ONNX captcha model files required by the default OCR method. If using `captchacracker`, the `model/weights.h5` file is used instead.
2.  **Install Dependencies**: Run the `pip install ...` commands listed in the **Prerequisites** section above for the core libraries and *at least one* OCR library. Use a [virtual environment](https://docs.python.org/3/library/venv.html) (`venv`) to manage dependencies cleanly.
    *   If you just want to use the default method (recommended), run:
    ```
    pip install requests numpy pillow colorama onnxruntime
    ```
3.  **Prepare the CSV File(s)**:
    *   Create one or more `.csv` files (e.g., `player_ids.csv`).
    *   **Format**: One ID per line OR comma-separated IDs are supported.
    *   Place the `.csv` file(s) in the same directory as the script, or note the full path.

4.  **Run the Script**: see below.

---

## Usage

Run the script from your command line or terminal using `python`:

```bash
python redeem_codes.py --code <gift_code> [--csv <path_or_pattern>] [--ocr-method <method>] [--save-images <mode>] [--use-gpu [id]]
```

### Arguments

-   `--code`: **Required**. The gift code you want to redeem (e.g., `WOS2025`).
-   `--csv`: Specifies the player ID source. Defaults to checking the current directory if not provided. Can be:
    *   A path to a single `.csv` file.
    *   A path to a folder/directory containing `.csv` files.
    *   The pattern `*.csv` (ensure quotes if needed by your shell) or `.` to process all `.csv` files in the script's directory.
-   `--ocr-method`: Selects the OCR engine. Choices depend on installed libraries (e.g., `onnx`, `ddddocr`, `easyocr`, `captchacracker`). Defaults to `onnx` if available, then `ddddocr`, then `captchacracker`, then `easyocr`.
-   `--save-images <mode>`: Controls saving captcha images to the `captcha_images` folder.
    *   `0`: None (Default)
    *   `1`: Failed CAPTCHAs only (OCR failure or server rejection)
    *   `2`: Successful CAPTCHAs only (Passed server validation)
    *   `3`: All CAPTCHAs
-   `--use-gpu [id]`: Enable GPU. Primarily affects `easyocr`. Optionally specify a PyTorch device ID (e.g., `--use-gpu 0`, `--use-gpu 1`). The ONNX model can also benefit from GPU via `onnxruntime-gpu`. `ddddocr`/`captchacracker` might auto-detect.

### Examples

*   **Process a gift code for all `.csv` files (using default ONNX model):**
    ```bash
    python redeem_codes.py --code ILoveWOS
    ```

*   **Process a specific `ids.csv`:**
    ```bash
    python redeem_codes.py --code ILoveWOS --csv ids.csv
    ```

*   **Process all `.csv` files using `ddddocr` as a fallback:**
    ```bash
    python redeem_codes.py --code ILoveWOS --ocr-method ddddocr
    ```

*   **Process all `.csv` files with ONNX, saving only successfully validated captcha images:**
    ```bash
    python redeem_codes.py --code ILoveWOS --csv *.csv --ocr-method onnx --save-images 2
    ```

*   **Process with `easyocr` using a specific GPU (e.g., discrete GPU with ID 1):**
    ```bash
    python redeem_codes.py --code ILoveWOS --csv all_ids.csv --ocr-method easyocr --use-gpu 1
    ```

---

## Features

-   **Multiple OCR Options**: Choose between different OCR engines:
    -   `onnx` (Recommended Default): Custom-trained ONNX model achieving very high speed and accuracy on WOS CAPTCHA. Lightweight, fast, and requires only `onnxruntime`, `numpy`, and `pillow`.
    -   `ddddocr`: Generic OCR library, lightweight and fast (~80% accuracy).
    -   `easyocr`: More robust OCR, potentially slower, offers GPU acceleration via PyTorch.
    -   `captchacracker`: Another model-based approach (requires TensorFlow and `model/weights.h5`).
-   **Flexible CSV Import**: Reads player IDs from `.csv` files. Supports **both** formats:
    -   One player ID per line.
    -   Multiple player IDs on a single line, separated by commas (whitespace is ignored).
-   **Automatic CAPTCHA Solving**: Uses the selected OCR method to automatically read and submit CAPTCHA codes required by the redemption API.
-   **Command-Line Interface**: Accepts the `.csv` file path (or a directory, or `*.csv`), gift code, and OCR method as arguments.
-   **Error Handling**: Provides clear error messages for missing/invalid inputs, API responses, and CAPTCHA failures.
-   **Retry Logic**: Automatically retries failed requests when the server indicates temporary issues (e.g., `TIMEOUT RETRY`) or CAPTCHA errors.
-   **Verbose Logging**: Shows timestamp, player nickname (if available) & ID consistently. Logs all output to a file (`redeemed_codes.txt`). Console output is colored for readability (requires `colorama`).
-   **CAPTCHA Image Saving**: Optionally saves CAPTCHA images to a folder (`captcha_images`) based on success/failure modes (`--save-images` flag).
-   **GPU Acceleration**: Optional GPU support primarily for `easyocr` (via PyTorch), with specific device selection.
-   **Summary Report**: Provides a summary of successful redemptions, already redeemed codes, errors, and detailed OCR/captcha statistics at the end, broken down by method used.

---

## GPU Support

GPU acceleration can speed up OCR processing. The `--use-gpu` flag primarily targets `easyocr`'s PyTorch backend, but the ONNX model can also benefit from GPU acceleration.

### How GPU Support Works

-   `onnx` uses ONNX Runtime. Install `onnxruntime-gpu` instead of `onnxruntime` to enable GPU acceleration via `CUDAExecutionProvider` or `DmlExecutionProvider` (DirectML on Windows). This usually happens automatically when the GPU package is installed.
-   `easyocr` uses PyTorch. The `--use-gpu [id]` flag tells PyTorch which CUDA device ID to use. For NVIDIA GPU you can find the device ID using the `nvidia-smi` command.
-   `ddddocr` uses ONNX Runtime internally. It can potentially use GPU providers if `onnxruntime-gpu` is installed.
-   `captchacracker` uses TensorFlow. TensorFlow typically auto-detects and uses compatible GPUs (CUDA).

### Setting Up NVIDIA GPU Support for EasyOCR

1.  **Install NVIDIA Drivers**: Ensure you have the latest drivers for your GPU.
2.  **Install CUDA Toolkit**: (Optional, often handled by PyTorch/TensorFlow install). If needed, install a compatible version (e.g., 11.8, 12.1) from NVIDIA's website.
3.  **Install PyTorch with CUDA support**: Use the command generator on the [PyTorch website](https://pytorch.org/get-started/locally/) for the correct `pip install` command corresponding to your OS and desired CUDA version. Example for CUDA 11.8:
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
4.  **Verify PyTorch GPU setup**: You could use the script `verify_gpu.py` included in this repository to verify GPU support.
    ```python
    python verify_gpu.py
    ```
    You will also see the main script output inform you if the GPU device is being used.

### Setting Up AMD GPU Support (ROCm for EasyOCR/PyTorch)

Support is more limited and depends on OS/GPU/ROCm version compatibility. Follow official ROCm and PyTorch guides.

### Using the Script with GPU Support

-   Use `--use-gpu` or `--use-gpu <id>` when running with `--ocr-method easyocr`.
-   For `onnx`, install `onnxruntime-gpu` to enable automatic GPU usage.
-   For `ddddocr` or `captchacracker`, GPU usage is typically automatic if dependencies are installed correctly; the `--use-gpu` flag will not have any effect.

---

## Output

### Sample Run

```plaintext
(Colorama adds colors in the actual terminal)
2025-05-06 10:30:01 - === Starting redemption script at 2025-05-06 10:30:01 ===
2025-05-06 10:30:01 - Gift Code: WOSNEWYEAR
2025-05-06 10:30:01 - Selected OCR Method: onnx
2025-05-06 10:30:01 - Save Images Mode: 1 (0:None, 1:Failed, 2:Success, 3:All)
...
2025-05-06 10:30:05 - Processing S123-PlayerOne(12345678) [1/150] for code: WOSNEWYEAR
2025-05-06 10:30:06 - PlayerOne(12345678) - [Attempt 1/4] Attempting OCR with onnx...
2025-05-06 10:30:06 - ONNX Result: AB3D
2025-05-06 10:30:06 - PlayerOne(12345678) - [Attempt 1/4] OCR successful using ONNX. Solved: AB3D
2025-05-06 10:30:07 - PlayerOne(12345678) - [Attempt 1/4] Server Response: Code 1, Msg 'RECEIVED'
2025-05-06 10:30:07 - PlayerOne(12345678) - Result: Already redeemed
2025-05-06 10:30:08 - Processing S456-PlayerTwo(87654321) [2/150] for code: WOSNEWYEAR
2025-05-06 10:30:09 - PlayerTwo(87654321) - [Attempt 1/4] Attempting OCR with onnx...
2025-05-06 10:30:09 - ONNX Result: EF7H
2025-05-06 10:30:09 - PlayerTwo(87654321) - [Attempt 1/4] OCR successful using ONNX. Solved: EF7H
2025-05-06 10:30:10 - PlayerTwo(87654321) - [Attempt 1/4] Server Response: Code 0, Msg 'SUCCESS'
2025-05-06 10:30:10 - PlayerTwo(87654321) - Result: Successfully redeemed
...
2025-05-06 10:45:00 - All 150/150 FIDs processed.
2025-05-06 10:45:00 -
========================= Redemption Summary =========================
2025-05-06 10:45:00 - Code Redeemed: WOSNEWYEAR
2025-05-06 10:45:00 - Total Unique FIDs Found: 150
2025-05-06 10:45:00 - Total FIDs Processed (Final Status Reached): 150
2025-05-06 10:45:00 -
--- Redemption Results ---
2025-05-06 10:45:00 - Successfully redeemed: 95
2025-05-06 10:45:00 - Already redeemed: 53
2025-05-06 10:45:00 - Code Expired / Limit Reached: 0
2025-05-06 10:45:00 - Other Errors/Failures: 2
2025-05-06 10:45:00 -
--- Error Details (FID: Last Error) ---
2025-05-06 10:45:00 -   11111111: Login failed: Account not found
2025-05-06 10:45:00 -   22222222: Max redemption attempts reached after Captcha Check Error.
2025-05-06 10:45:00 -
========================= Captcha Statistics =========================
2025-05-06 10:45:00 - OCR Method Used: onnx
2025-05-06 10:45:00 - Total Captcha Fetches Attempted: 155
2025-05-06 10:45:00 - Total OCR Recognition Calls: 155
2025-05-06 10:45:00 - Successful OCR (Valid Format): 153
2025-05-06 10:45:00 -   └─ ONNX Successes: 153
2025-05-06 10:45:00 - Total Captcha Submissions (Attempts Sent to Server): 153
2025-05-06 10:45:00 -   ├─ Passed Server Validation: 150
2025-05-06 10:45:00 -   └─ Failed Server Validation: 3
2025-05-06 10:45:00 - Rate Limited Events (Fetch/Redeem): 1
2025-05-06 10:45:00 -
OCR Success Rate (Valid Format / OCR Calls): 98.71%
2025-05-06 10:45:00 - Server Pass Rate (Passed / Total Submissions): 98.04%
2025-05-06 10:45:00 - Captcha images saved to: captcha_images
2025-05-06 10:45:00 -
Total execution time: 0:14:59
======================================================================
```

### Logging

All console output (without color codes) is automatically appended to a log file named `redeemed_codes.txt` in the script folder.

If `--save-images` is set to 1, 2, or 3, a folder named `captcha_images` will be created to save captcha images.

---

## Troubleshooting

1.  **`pip` command not found**: Ensure Python is installed correctly and in PATH.
2.  **ModuleNotFoundError**: Make sure you've installed the core libraries (`requests`, `numpy`, `pillow`, `colorama`) and at least *one* of the required OCR libraries (`onnxruntime`, `ddddocr`, `easyocr`, `captchacracker`) in your active Python environment/venv. The `opencv-python` package is only needed for `ddddocr`, `easyocr`, and `captchacracker` methods. Check for install errors.
3.  **`onnxruntime` Issues**: Errors during ONNX model initialization might stem from `onnxruntime` problems (missing DLLs, incompatible CPU instructions). Ensure `onnxruntime` installed correctly. Also verify that the model files (`model/captcha_model.onnx` and `model/captcha_model_metadata.json`) exist in the `model/` directory.
4.  **`ddddocr` Issues**: `ddddocr` relies on `onnxruntime` internally. Errors during `ddddocr` initialization might stem from `onnxruntime` problems.
5.  **`captchacracker` / `tensorflow` Issues**: This method depends heavily on a correct TensorFlow installation, which can be complex (CPU vs GPU versions, CUDA/cuDNN dependencies, DLL issues, Python version compatibility). If the script fails to import `CaptchaCracker`, try importing `tensorflow` directly in a Python interpreter within the venv to diagnose. Ensure the `model/weights.h5` file exists.
6.  **`easyocr` / `torch` Issues**: Ensure PyTorch and its dependencies (`torchvision`, `torchaudio`) are installed correctly, matching your system (CPU/CUDA version).
7.  **CSV File Not Found**: Verify the `--csv` path.
8.  **Permission Denied (Log File / CAPTCHA Folder)**: Check write permissions.
9.  **Code Expired / Claim Limit Reached**: Verify the gift code.
10. **API Rate Limiting / `TIMEOUT RETRY`**: Increase `DELAY` in the script if needed.
11. **CAPTCHA Solving Failures (`CAPTCHA CHECK ERROR`, etc.)**:
    *   The selected OCR method might be struggling. Try a different one (`--ocr-method`). The `onnx` method is recommended first.
    *   If using `easyocr`, ensure it's installed correctly and consider trying GPU acceleration.
    *   Check saved failed images (`--save-images 1` or `3`) to see if the captcha is readable. The API might have changed captcha style.
12. **GPU Issues**:
    *   Verify CUDA/ROCm setup and matching PyTorch/TensorFlow versions.
    *   Try different device IDs with `--use-gpu`.
    *   Run without `--use-gpu` to test CPU fallback.

---

## Changelog

### v4.0.0 (Current)

-   Added custom-trained ONNX captcha model as the new default OCR method (~98% accuracy)
-   New OCR priority: `onnx` > `ddddocr` > `captchacracker` > `easyocr`
-   ONNX method requires only `onnxruntime`, `numpy`, and `pillow` — no `opencv-python` needed
-   Improved browser header spoofing with randomized Chrome versions and proper `sec-*` headers
-   Model files included in `model/` directory (`captcha_model.onnx`, `captcha_model_metadata.json`)

### v3.0.5
-   Uploaded a better Captchacracker model (trained on ~10k validated captchas)
-   Reduced the character set to check for since the Gift API is case-insensitive

### v3.0.0 
-   Refactored, streamlined OCR calling logic, updated summary statistics.
-   Added support for `ddddocr` (default/recommended) and `captchacracker` alongside `easyocr`. Select via `--ocr-method`.
-   Replaced `--all-images` with `--save-images [0|1|2|3]` for more control over saving successful/failed captchas to `captcha_images` folder.
-   Successfully validated codes will be saved as `<code>.png` and unsuccessful ones as `FAIL_<fid>_<timestamp>.png` depending on `--save-images` settings.
-   Added colored console output (requires `colorama`), consistent `Nickname (FID)` prefix, specific log levels.

### v2.4.5
-   Added support for discrete GPUs with device selection via `--use-gpu` parameter
-   Improved GPU error handling with graceful fallback to CPU

### v2.4.0
-   Added improved CAPTCHA preprocessing with multiple image enhancement techniques
-   Added comprehensive captcha statistics in summary output
-   Added progress tracking with current/total indicators
-   Added detailed error reporting by player ID
-   Added execution time tracking and reporting
-   Added final unprocessed ID check to guarantee all IDs are eventually processed
-   Improved retry queue handling for rate-limited IDs
-   Added option to disable captcha image saving to conserve disk space
-   Fixed issues with counting and reporting

### v2.3.0
-   Integrated OCR (EasyOCR) to automatically read and submit CAPTCHA codes required by the redemption API.
-   Added `easyocr`, `opencv-python`, `numpy`, and PyTorch (`torch`, `torchvision`, `torchaudio`) for OCR.
-   Saves attempted CAPTCHA images with OCR results in the filename to a subfolder (`failed_captchas`) for debugging.
-   Enhanced retry logic specifically for CAPTCHA-related errors (`CAPTCHA CHECK ERROR`, `Sign Error`, `CAPTCHA CHECK TOO FREQUENT`).

### v2.2.0
-   Added support for reading comma-separated player IDs within CSV files.
-   Improved CSV file path handling in `--csv` argument (folder path, `*.csv` pattern).
-   Enhanced logging detail and error categorization.

### v2.1.0
-   Added support for processing all .csv files in a folder or the script's directory using `*.csv`.
-   Improved error handling for missing or invalid .csv files.

### v2.0.0
-   Added retry logic for failed requests (e.g., `TIMEOUT RETRY`).
-   Display player nicknames during processing.
-   Added Unicode support for special characters and foreign alphabets.
-   Added a summary report of redemptions at the end.
-   Improved error handling and logging.

### v1.0.0 (Initial Release)
-   Basic functionality: CSV import (newline separated), command-line args, API requests.
-   Initial error handling and rate limiting.

---

## Credits

-   **Author**: justncodes (\[SIR\] Yolo on #340) - [Repository](https://github.com/justncodes/wos-giftcode)
-   **OCR Libraries**: [ONNX Runtime](https://github.com/microsoft/onnxruntime), [ddddocr](https://github.com/sml2h3/ddddocr), [EasyOCR](https://github.com/JaidedAI/EasyOCR), [CaptchaCracker](https://github.com/kerlomz/CaptchaCracker)

---

## Support

If you encounter any issues or have questions, feel free to open an issue and include relevant logs, script version, and chosen OCR method.

---

## License

This project is licensed under the GPLv3 License. See the `LICENSE` file for details.
