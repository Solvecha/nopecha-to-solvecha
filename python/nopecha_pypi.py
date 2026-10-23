"""PyPI `nopecha` package (tested with 2.0.1) against Solvecha.

The only change to a NopeCHA script: the `host` of the client class.

    python nopecha_pypi.py tile1.jpg tile2.jpg ...      # reCAPTCHA: 1 to 9 tile pictures
    python nopecha_pypi.py                              # text captcha from ../assets/text-captcha.png
"""
import base64
import os
import sys
from pathlib import Path

from nopecha.api.requests import RequestsAPIClient


class SolvechaClient(RequestsAPIClient):
    host = "https://api.solvecha.com"  # was "https://api.nopecha.com"


def b64(path: str | Path) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()


client = SolvechaClient(os.environ["SOLVECHA_API_KEY"])
print("status:", client.status())

if sys.argv[1:]:
    # One answer per tile picture: True means "select this tile".
    print("recaptcha:", client.recognize_recaptcha("Select all images with a fire hydrant", [b64(p) for p in sys.argv[1:]]))
else:
    text_picture = Path(__file__).parent.parent / "assets" / "text-captcha.png"
    print("textcaptcha:", client.recognize_raw({"type": "textcaptcha", "image_data": [b64(text_picture)]}))
