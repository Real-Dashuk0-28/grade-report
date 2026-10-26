from collections import defaultdict


def calculate_statistics(students):
    if not students:
        return {
            "student_count": 0,
            "average_score": 0.0,
            "min_score": None,
            "max_score": None,
            "group_averages": {},
        }

    scores = [student["score"] for student in students]
    groups = defaultdict(list)

    for student in students:
        groups[student["group"]].append(student["score"])

    return {
        "student_count": len(students),
        "average_score": round(sum(scores) / len(scores), 2),
        "min_score": min(scores),
        "max_score": max(scores),
        "group_averages": {
            group: round(sum(values) / len(values), 2)
            for group, values in sorted(groups.items())
        },
    }
