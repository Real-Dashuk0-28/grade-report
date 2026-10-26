import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from grade_report.reader import read_students
from grade_report.statistics import calculate_statistics

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Анализатор успеваемости студентов"
    )
    parser.add_argument("csv_file", help="Путь к исходному CSV-файлу")
    parser.add_argument(
        '--output',
        required=True,
        help="Путь к выходному JSON файлу",
    )
    args = parser.parse_args()

    try:
        students = read_students(args.csv_file)

        if not students:
            console.print("В файле отсутствуют данные студентов.")
            return 0
        result = calculate_statistics(students)

        table = Table(title="Анализ успеваемости")
        table.add_column("Показатель")
        table.add_column("Значение", justify="right")

        table.add_row("Количество студентов", str(result["student_count"]))
        table.add_row("Средний балл", f'{result["average_score"]:.2f}')
        table.add_row("Минимальный балл", str(result["min_score"]))
        table.add_row("Максимальный балл", str(result["max_score"]))

        for group, average in result["group_averages"].items():
            table.add_row(
                f'Средний балл группы {group}',
                f"{average:.2f}",
            )
        console.print(table)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        console.print(f"[green]Отчёт сохранён: {output_path}[/green]")
        return 0
    except (FileNotFoundError, ValueError, OSError) as error:
        console.print(f"[red]Ошибка: {error}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())

