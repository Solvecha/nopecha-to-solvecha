"""PyPI `python3-capsolver` package (tested with 1.2.2) against Solvecha.

The only change to a CapSolver script: `request_url`.

    python python3_capsolver_example.py grid.jpg "/m/01pns0"
    python python3_capsolver_example.py
"""
import base64
import os
import sys
from pathlib import Path

from python3_capsolver.core.enum import CaptchaTypeEnm
from python3_capsolver.image_to_text import ImageToText
from python3_capsolver.recaptcha import ReCaptcha

KEY = os.environ["SOLVECHA_API_KEY"]
URL = "https://api.solvecha.com"  # request_url: was the CapSolver address
b64 = lambda path: base64.b64encode(Path(path).read_bytes()).decode()  # noqa: E731

if len(sys.argv) >= 3:
    solver = ReCaptcha(api_key=KEY, captcha_type=CaptchaTypeEnm.ReCaptchaV2Classification, request_url=URL)
    print("grid:", solver.captcha_handler(task_payload={"image": b64(sys.argv[1]), "question": sys.argv[2]}))
else:
    text_picture = Path(__file__).parent.parent / "assets" / "text-captcha.png"
    solver = ImageToText(api_key=KEY, request_url=URL)
    print("text:", solver.captcha_handler(task_payload={"body": b64(text_picture), "module": "common"}))
