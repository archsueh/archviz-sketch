#!/usr/bin/env python3
"""
grok_image.py — direct xAI (Grok) image generation. No Hermes, no SDK, stdlib only.

The API key is read from the XAI_API_KEY environment variable. It is NEVER passed
on the command line (so it won't leak into shell history) and never written to disk.

Endpoint: POST https://api.x.ai/v1/images/generations  (OpenAI-compatible)
Models evolve fast — default is grok-2-image; override with --model, or run
--list-models to discover what your account currently has.

Usage:
    export XAI_API_KEY=...            # set once in your shell / .zshrc / .env
    python3 grok_image.py --prompt "a cat in a tree" --out cat.jpg
    python3 grok_image.py --prompt-file prompt.txt --out out.jpg --model grok-2-image
    archviz-sketch generate -s xiaohei --subject "三层架构" | \
        python3 grok_image.py --prompt-file - --out fig01.jpg
    python3 grok_image.py --list-models

Pipeline role: pair with `archviz-sketch generate` (which produces the prompt).
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API_BASE = "https://api.x.ai/v1"
DEFAULT_MODEL = "grok-2-image"


def _key() -> str:
    k = os.environ.get("XAI_API_KEY", "").strip()
    if not k:
        sys.exit("error: XAI_API_KEY is not set. `export XAI_API_KEY=...` first "
                 "(do not pass the key as an argument).")
    return k


def _request(method: str, path: str, payload: dict | None = None) -> dict:
    url = f"{API_BASE}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {_key()}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"error: HTTP {e.code} from xAI — {body}")
    except urllib.error.URLError as e:
        sys.exit(f"error: cannot reach {url} — {e.reason}")


def list_models() -> None:
    out = _request("GET", "/models")
    ids = [m.get("id", "") for m in out.get("data", [])]
    img = [i for i in ids if "image" in i.lower() or "imagine" in i.lower()]
    print("image-capable models:", img or "(none flagged — try grok-2-image)")
    print("all models:", ids)


def generate(prompt: str, out: str, model: str, n: int) -> None:
    payload = {"model": model, "prompt": prompt, "n": n, "response_format": "b64_json"}
    res = _request("POST", "/images/generations", payload)
    items = res.get("data", [])
    if not items:
        sys.exit(f"error: no image returned. Raw: {json.dumps(res)[:400]}")
    for i, item in enumerate(items):
        target = out if n == 1 else _index_path(out, i + 1)
        if item.get("b64_json"):
            with open(target, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            with urllib.request.urlopen(item["url"], timeout=120) as r, open(target, "wb") as f:
                f.write(r.read())
        else:
            sys.exit(f"error: item {i} had neither b64_json nor url. {json.dumps(item)[:200]}")
        revised = item.get("revised_prompt")
        print(f"saved {target}" + (f"  (revised_prompt: {revised[:80]}…)" if revised else ""))


def _index_path(path: str, i: int) -> str:
    root, dot, ext = path.rpartition(".")
    return f"{root}-{i:02d}.{ext}" if dot else f"{path}-{i:02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Direct xAI Grok image generation (stdlib only).")
    ap.add_argument("--prompt", help="Prompt text.")
    ap.add_argument("--prompt-file", help="Read prompt from file, or '-' for stdin.")
    ap.add_argument("--out", "-o", default="grok-image.jpg", help="Output path (jpg).")
    ap.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model id (default {DEFAULT_MODEL}).")
    ap.add_argument("--n", type=int, default=1, help="Number of images (default 1).")
    ap.add_argument("--list-models", action="store_true", help="List available models and exit.")
    args = ap.parse_args()

    if args.list_models:
        list_models()
        return

    if args.prompt_file == "-":
        prompt = sys.stdin.read().strip()
    elif args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read().strip()
    elif args.prompt:
        prompt = args.prompt.strip()
    else:
        ap.error("provide --prompt, --prompt-file, or --prompt-file - (stdin).")

    if not prompt:
        sys.exit("error: empty prompt.")
    generate(prompt, args.out, args.model, args.n)


if __name__ == "__main__":
    main()
