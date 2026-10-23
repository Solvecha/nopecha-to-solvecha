<p align="center">
  <a href="https://solvecha.com"><img src="https://solvecha.com/site/static/apple-touch-icon.png" width="64" height="64" alt="Solvecha"></a>
</p>

<h1 align="center">NopeCHA to Solvecha</h1>

<p align="center">
  Switch an existing NopeCHA (or CapSolver image) integration to <a href="https://solvecha.com">Solvecha</a> by changing one setting.<br>
  Runnable Python, Node.js and curl examples, tested against the live API.
</p>

<p align="center">
  <a href="https://github.com/Solvecha/nopecha-to-solvecha/actions/workflows/ci.yml"><img src="https://github.com/Solvecha/nopecha-to-solvecha/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT license"></a>
  <a href="https://pypi.org/project/nopecha/"><img src="https://img.shields.io/badge/PyPI-nopecha%202.0.1-3775A9.svg" alt="PyPI nopecha"></a>
  <a href="https://www.npmjs.com/package/nopecha"><img src="https://img.shields.io/badge/npm-nopecha%201.0.11-CB3837.svg" alt="npm nopecha"></a>
  <a href="https://solvecha.com"><img src="https://img.shields.io/badge/Solvecha-free%20tier%20100%2Fday-5b5bd6.svg" alt="Solvecha free tier"></a>
</p>

---

Solvecha answers image captchas. It takes the same requests as the NopeCHA recognition API and, for two task types, the CapSolver API. For most scripts the whole migration is: **new base URL, new key.**

> Solvecha returns **answers for the pictures you send** (which tiles, which text). It does not return finished reCAPTCHA tokens. If you used the NopeCHA or CapSolver *token* APIs, they have no equivalent here. Use the [browser extension](https://github.com/Solvecha/solvecha-extension) to click the tiles in a real browser.

## Which package, which setting

Each row was run against `https://api.solvecha.com` on 23 October 2026 with a real reCAPTCHA grid picture and a text picture.

| Package | Version tested | Setting | reCAPTCHA grid | Text picture |
|---|---|---|---|---|
| [`nopecha` (PyPI)](https://pypi.org/project/nopecha/) | 2.0.1 | `host = "https://api.solvecha.com"` in a subclass | works (`recognize_recaptcha`, 1 to 9 tile pictures) | works (`recognize_raw`, type `textcaptcha`) |
| [`nopecha` (npm)](https://www.npmjs.com/package/nopecha) | 1.0.11 | `apiBase: "https://api.solvecha.com"` | works (`solveRecognition`, type `recaptcha`) | works (type `textcaptcha`) |
| [`capsolver` (PyPI)](https://pypi.org/project/capsolver/) | 1.0.7 | `CAPSOLVER_API_BASE=https://api.solvecha.com` or `capsolver.api_base` | works (`ReCaptchaV2Classification`) | works (`ImageToTextTask`) |
| [`python3-capsolver` (PyPI)](https://pypi.org/project/python3-capsolver/) | 1.2.2 | `request_url="https://api.solvecha.com"` | works (`ReCaptchaV2Classification`) | works (`ImageToTextTask`) |

Plain HTTP works too: see [`curl/nopecha_style.sh`](curl/nopecha_style.sh).

## Quick start

1. Create a free account on [solvecha.com](https://solvecha.com/register) and copy the key from the [dashboard](https://solvecha.com/dashboard). The free tier has 100 successful solves per day.
2. `export SOLVECHA_API_KEY=slv_...` (never commit a key).
3. Run an example.

### PyPI `nopecha`

```python
from nopecha.api.requests import RequestsAPIClient

class SolvechaClient(RequestsAPIClient):
    host = "https://api.solvecha.com"  # was https://api.nopecha.com

client = SolvechaClient(os.environ["SOLVECHA_API_KEY"])
client.recognize_recaptcha("Select all images with a fire hydrant", tile_images_b64)  # [False, True, ...]
client.recognize_raw({"type": "textcaptcha", "image_data": [image_b64]})              # {"data": ["x7Kp2"]}
```

```bash
cd python && pip install -r requirements.txt
python nopecha_pypi.py                       # text captcha from assets/
python nopecha_pypi.py tile1.jpg tile2.jpg   # reCAPTCHA tile pictures
```

### npm `nopecha`

```js
const { Configuration, NopeCHAApi } = require("nopecha");

const nopecha = new NopeCHAApi(new Configuration({
  apiKey: process.env.SOLVECHA_API_KEY,
  apiBase: "https://api.solvecha.com", // was https://api.nopecha.com
}));
await nopecha.solveRecognition({ type: "recaptcha", task: "Select all images with a fire hydrant", image_data: [gridImageBase64] });
```

```bash
cd node && npm install
node nopecha_npm.mjs grid.jpg
```

### PyPI `capsolver`

```python
import os
os.environ["CAPSOLVER_API_BASE"] = "https://api.solvecha.com"  # before the import
import capsolver

capsolver.api_key = os.environ["SOLVECHA_API_KEY"]
capsolver.solve({"type": "ReCaptchaV2Classification", "image": image_b64, "question": "/m/01pns0"})
# {"objects": [1], "size": 1, "type": "multi"}   tile numbers start at 0
capsolver.solve({"type": "ImageToTextTask", "module": "common", "body": image_b64})
```

```bash
python python/capsolver_pypi.py grid.jpg "/m/01pns0"
```

### PyPI `python3-capsolver`

See [`python/python3_capsolver_example.py`](python/python3_capsolver_example.py). The one change is `request_url="https://api.solvecha.com"`.

## What stays the same, what differs

| | NopeCHA | CapSolver | Solvecha |
|---|---|---|---|
| Create, poll, status | `POST /`, `GET /?id=`, `/v1/recognition/<type>`, `/status` | `createTask`, `getTaskResult`, `getBalance` | Same paths and fields, error codes `9`, `10`, `11`, `14`, `15`, `16` |
| Key | Header, body or query | `clientKey` | Same three ways, and `clientKey` |
| Supported types | many | many | reCAPTCHA v2 image grids, text pictures, GeeTest slider, FunCAPTCHA. For CapSolver only `ReCaptchaV2Classification` and `ImageToTextTask`. Everything else answers `ERROR_TASK_NOT_SUPPORTED` |
| Tokens | yes (separate API) | yes | **no** |
| Request body | JSON | JSON | JSON or url-encoded form. No multipart |
| Daily quota reset | rolling 24 hours | n/a | 00:00 UTC |

Good to know:

- reCAPTCHA pictures go in `image_data` as base64. Solvecha does not download `image_urls`.
- Without `grid`, several pictures count as single tiles. One picture is read by its size: up to 160 px one tile, up to 380 px a 3x3 grid, larger a 4x4 grid. Send `grid` yourself to be exact.
- CapSolver `question` takes a reCAPTCHA object code (`/m/01pns0`) or the instruction in words.
- Full details: [Migrating from NopeCHA](https://solvecha.com/docs/migrate-from-nopecha) and [Migrating from CapSolver](https://solvecha.com/docs/migrate-from-capsolver).

## Prices

Only figures that Solvecha publishes on [solvecha.com/compare](https://solvecha.com/compare) with their sources. The competitor figures were read on 16 October 2026. Check the sources again before you decide.

| Monthly plan (solves per day) | Solvecha | NopeCHA, billed monthly |
|---|---|---|
| Starter (2,000) | $2.49 | $4.99 |
| Basic (20,000) | $9.99 | $19.99 |
| Professional (80,000) | $24.99 | $49.99 |
| Enterprise (200,000) | $49.99 | $99.99 |

| Pay per use, per 1,000 reCAPTCHA image solves | Price |
|---|---|
| Solvecha | $0.10 |
| CapSolver `ReCaptchaClassification` ([docs.capsolver.com/en/pricing](https://docs.capsolver.com/en/pricing)) | $0.40 |

Solvecha also has a free tier of 100 successful solves per day. NopeCHA source: [nopecha.com/pricing](https://nopecha.com/pricing). Solvecha prices are net: VAT is added at checkout where it applies.

Quality: 99.7 % of sessions on Google's public reCAPTCHA demo got a token within 3 tries (299 of 300 sessions, 17 October 2026, one data-center IP). Other sites and IPs can differ. Method and raw numbers: [solvecha.com/compare](https://solvecha.com/compare).

## Browser instead of API?

If you drove a browser with the NopeCHA extension, see [solvecha-playwright-example](https://github.com/Solvecha/solvecha-playwright-example) (Playwright, Puppeteer and Selenium with the Solvecha extension).

## Links

[Website](https://solvecha.com) · [Docs](https://solvecha.com/docs) · [Agent skills](https://github.com/Solvecha/solvecha-skills) · [Extension](https://github.com/Solvecha/solvecha-extension)

MIT licensed. Solvecha is not affiliated with NopeCHA, CapSolver or Google.
