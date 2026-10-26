import csv
from pathlib import Path

REQUIRED_COLUMNS = {"student", "group", "score"}


def read_students(path):
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with file_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("CSV-файл пустой: отсутствует заголовок.")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(
                "отсутствуют обязательные столбцы: "
                + ", ".join(sorted(missing))
            )
        students = []

        for line_number, row in enumerate(reader, start=2):
            student = (row.get("student") or "").strip()
            group = (row.get("group") or "").strip()
            raw_score = (row.get("score") or "").strip()

            if not student or not group or not raw_score:
                raise ValueError(f"Строка {line_number}: обнаружено пустое поле.")

            try:
                score = int(raw_score)
            except ValueError:
                raise ValueError(
                    f"Строка {line_number}:"
                    "балл должен быть целым числом."
                ) from None
            if not 0 <= score <= 100:
                raise ValueError(
                    f"Строка {line_number}:"
                    "балл должен быть от 0 до 100."
                )
            students.append({
                "student": student,
                "group": group,
                "score": score,
            })
    return students
