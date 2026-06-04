# Whiteout Survival Gift Code Redemption Script

A Python CLI tool that automates redeeming gift codes in the mobile game **Whiteout Survival**. It reads player IDs from CSV files, solves CAPTCHAs automatically using a custom ONNX model, and submits redemption requests via the game's API.

## Usage

Run from the console workflow or Shell:

```bash
python redeem_codes.py --code <GIFT_CODE> [--csv <path>] [--ocr-method <method>] [--save-images <0-3>]
```

### Required argument
- `--code` — the gift code to redeem (e.g. `WOS2025`)

### Optional arguments
- `--csv` — path to a CSV file, directory of CSV files, or `*.csv` pattern (defaults to current directory)
- `--ocr-method` — OCR engine: `onnx` (default, ~98%), `ddddocr` (~80%), `easyocr`, `captchacracker`
- `--save-images` — save captcha images: `0`=none, `1`=failed, `2`=success, `3`=all
- `--use-gpu` — enable GPU acceleration (mainly for `easyocr`)

### CSV format
One player ID per line, or comma-separated IDs on each line.

### Example
```bash
python redeem_codes.py --code ILoveWOS --csv player_ids.csv
```

## Dependencies installed
- `requests`, `numpy`, `pillow`, `colorama` — core libraries
- `onnxruntime` — default ONNX captcha model (recommended)
- `opencv-python` — required for ddddocr/easyocr/captchacracker methods

## Model files
- `model/captcha_model.onnx` — ONNX captcha model
- `model/captcha_model_metadata.json` — model metadata

## Output
- Console output with colored logs
- `redeemed_codes.txt` — log file appended after each run
- `captcha_images/` — saved captcha images (if `--save-images` > 0)

## User preferences
