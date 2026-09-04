#!/usr/bin/env python3
"""
Aeterna Rewrite Engine — CLI Client
Open Core Interface for local text processing models.
"""

import sys
import os
import argparse
import json
import subprocess
import tempfile

def parse_args():
    parser = argparse.ArgumentParser(
        description="Aeterna Rewrite Engine CLI — Open Core Interface"
    )
    parser.add_argument(
        "--file", "-f",
        help="Путь к входному текстовому файлу (UTF-8)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Путь для сохранения результата"
    )
    parser.add_argument(
        "--style", "-s",
        default="Лёгкий",
        choices=["Лёгкий", "Углублённый", "Художественный"],
        help="Стиль обработки текста"
    )
    parser.add_argument(
        "--mode", "-m",
        default="Рерайт",
        choices=["Рерайт", "Структура"],
        help="Режим работы ядра"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Температура генерации (0.1 - 1.0)"
    )
    parser.add_argument(
        "--no-synergy",
        action="store_true",
        help="Отключить многопроходную оптимизацию контекста"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Вывод результата и метаданных в формате JSON"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    binary_candidates = [
        os.path.join(script_dir, "Aeterna_Rewrite_Engine"),
        os.path.join(os.getcwd(), "Aeterna_Rewrite_Engine")
    ]
    binary_path = next((p for p in binary_candidates if os.path.isfile(p)), None)

    temp_input = None
    input_path = args.file

    if not input_path:
        if sys.stdin.isatty():
            print("Введите текст (Ctrl+D для завершения):", file=sys.stderr)
        text = sys.stdin.read()
        if not text.strip():
            print("Ошибка: пустой ввод", file=sys.stderr)
            sys.exit(1)
        tfile = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False)
        tfile.write(text)
        tfile.close()
        input_path = tfile.name
        temp_input = input_path
    else:
        if not os.path.exists(input_path):
            print(f"Ошибка: входной файл не найден: {input_path}", file=sys.stderr)
            sys.exit(1)

    try:
        if binary_path:
            cmd = [
                binary_path,
                "cli",
                "--file", input_path,
                "--style", args.style,
                "--mode", args.mode
            ]
            if args.output:
                cmd.extend(["--output", args.output])

            proc = subprocess.run(cmd, capture_output=(args.output is None or args.json), text=True)
            if proc.returncode != 0:
                if proc.stderr:
                    print(proc.stderr, file=sys.stderr)
                sys.exit(proc.returncode)

            if args.output is None:
                if args.json:
                    res = {
                        "status": "success",
                        "mode": args.mode,
                        "style": args.style,
                        "engine": "Aeterna SynergyCore (Standalone)",
                        "output": proc.stdout.strip()
                    }
                    print(json.dumps(res, ensure_ascii=False, indent=2))
                else:
                    print(proc.stdout)
        else:
            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()
            preview = f"[Aeterna Open-Core Preview]: Ядро SynergyCore не найдено. Входной текст ({len(content)} симв.) готов к обработке в режиме '{args.mode}' ({args.style})."
            if args.json:
                res = {
                    "status": "preview",
                    "mode": args.mode,
                    "style": args.style,
                    "engine": "Open-Core Staging",
                    "output": preview
                }
                output_text = json.dumps(res, ensure_ascii=False, indent=2)
            else:
                output_text = preview

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output_text)
            else:
                print(output_text)
    finally:
        if temp_input and os.path.exists(temp_input):
            os.remove(temp_input)

if __name__ == "__main__":
    main()
