// npm `nopecha` package (tested with 1.0.11) against Solvecha.
// The only change to a NopeCHA script: `apiBase`.
//
//   node nopecha_npm.mjs grid.jpg      # reCAPTCHA: one picture of the whole 3x3 or 4x4 grid
//   node nopecha_npm.mjs               # text captcha from ../assets/text-captcha.png
import { createRequire } from "node:module";
import { readFile } from "node:fs/promises";

const { Configuration, NopeCHAApi } = createRequire(import.meta.url)("nopecha"); // the package is CommonJS

const nopecha = new NopeCHAApi(
  new Configuration({
    apiKey: process.env.SOLVECHA_API_KEY,
    apiBase: "https://api.solvecha.com", // was "https://api.nopecha.com"
  }),
);

const b64 = async (path) => (await readFile(path)).toString("base64");
console.log("status:", await nopecha.getBalance());

if (process.argv[2]) {
  // `grid` is optional: without it the size of the picture decides (3x3 or 4x4).
  console.log("recaptcha:", await nopecha.solveRecognition({
    type: "recaptcha",
    task: "Select all images with a fire hydrant",
    image_data: [await b64(process.argv[2])],
  }));
} else {
  const picture = new URL("../assets/text-captcha.png", import.meta.url);
  console.log("textcaptcha:", await nopecha.solveRecognition({ type: "textcaptcha", image_data: [await b64(picture)] }));
}
