"""archviz-sketch CLI."""

import argparse
import sys
from pathlib import Path
from .engine import get_prompt, list_styles


def main():
    parser = argparse.ArgumentParser(prog="archviz-sketch", description="Sketch illustration pipeline")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List sketch styles")

    p_gen = sub.add_parser("generate", help="Generate a sketch prompt")
    p_gen.add_argument("--style", "-s", required=True)
    p_gen.add_argument("--subject", required=True)
    p_gen.add_argument("--output", "-o", help="Output file")

    args = parser.parse_args()

    if args.command == "list":
        for s in list_styles():
            print(f"  {s['style']:25s} {s['description']}")
    elif args.command == "generate":
        prompt = get_prompt(args.style, {"subject": args.subject})
        if args.output:
            Path(args.output).write_text(prompt)
            print(f"Written to {args.output}")
        else:
            print(prompt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
