"""PyPI `capsolver` package (tested with 1.0.7) against Solvecha.

The only change to a CapSolver script: the base URL. Set it before the import.

    python capsolver_pypi.py grid.jpg "/m/01pns0"   # ReCaptchaV2Classification (object code or words)
    python capsolver_pypi.py                        # ImageToTextTask from ../assets/text-captcha.png
"""
import base64
import os
import sys
from pathlib import Path

os.environ["CAPSOLVER_API_BASE"] = "https://api.solvecha.com"  # was https://api.capsolver.com

import capsolver  # noqa: E402  (after the environment variable on purpose)

capsolver.api_key = os.environ["SOLVECHA_API_KEY"]
# Or without the environment variable: capsolver.api_base = "https://api.solvecha.com"

b64 = lambda path: base64.b64encode(Path(path).read_bytes()).decode()  # noqa: E731

print("balance:", capsolver.balance())
if len(sys.argv) >= 3:
    # solution["objects"] holds the selected tiles, counted from 0.
    print("grid:", capsolver.solve({"type": "ReCaptchaV2Classification", "image": b64(sys.argv[1]), "question": sys.argv[2]}))
else:
    text_picture = Path(__file__).parent.parent / "assets" / "text-captcha.png"
    print("text:", capsolver.solve({"type": "ImageToTextTask", "module": "common", "body": b64(text_picture)}))
