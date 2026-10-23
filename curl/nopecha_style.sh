#!/usr/bin/env bash
# NopeCHA-style calls with plain curl. Needs: curl, jq, base64.
#   ./nopecha_style.sh text ../assets/text-captcha.png
#   ./nopecha_style.sh grid grid.jpg 3x3 "Select all images with a fire hydrant"
set -euo pipefail
API=https://api.solvecha.com
: "${SOLVECHA_API_KEY:?Set SOLVECHA_API_KEY}"
auth=(-H "Authorization: Bearer $SOLVECHA_API_KEY" -H "Content-Type: application/json")

case "$1" in
  text) body=$(jq -n --arg img "$(base64 -w0 "$2")" '{image_data: [$img]}'); path=/v1/recognition/textcaptcha ;;
  grid) body=$(jq -n --arg img "$(base64 -w0 "$2")" --arg grid "$3" --arg task "$4" '{task: $task, grid: $grid, image_data: [$img]}'); path=/v1/recognition/recaptcha ;;
  *) echo "usage: text <image> | grid <image> <3x3|4x4> <task text>"; exit 2 ;;
esac

# sync=1: the answer comes back in the same request (up to 15 seconds).
curl -fsS "${auth[@]}" -d "$body" "$API$path?sync=1"
echo
