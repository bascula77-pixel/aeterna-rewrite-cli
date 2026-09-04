#!/usr/bin/env python3
"""
Aeterna Rewrite Engine — CLI Client
Open Core Interface for local text processing models.
"""

import sys
import os
import argparse
import json
import time

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

    if args.file:
        if not os.path.exists(args.file):
            print(f"Ошибка: входной файл не найден: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        if sys.stdin.isatty():
            print("Введите текст (Ctrl+D для завершения):", file=sys.stderr)
        text = sys.stdin.read()

    if not text.strip():
        print("Ошибка: пустой ввод", file=sys.stderr)
        sys.exit(1)

    start_time = time.time()

    # Интерфейсный слой Open-Core.
    # В дистрибутиве с Kwork этот блок обращается к локальному скомпилированному ядру SynergyCore.
    result = {
        "status": "success",
        "mode": args.mode,
        "style": args.style,
        "synergy_enabled": not args.no_synergy,
        "input_length": len(text),
        "output": f"[Aeterna Open-Core Preview]: Обработано {len(text)} симв. в режиме '{args.mode}' ({args.style}).",
        "telemetry": {
            "inference_time_sec": round(time.time() - start_time, 3),
            "engine": "Aeterna SynergyCore (Standalone)"
        }
    }

    if args.json:
        output_text = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output_text = result["output"]

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[AETERNA] Результат сохранен в {args.output}", file=sys.stderr)
    else:
        print(output_text)

if __name__ == "__main__":
    main()
