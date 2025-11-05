# log_analyzer.py
import re
from collections import Counter
from typing import Tuple, List

LOG_LEVELS = ("INFO", "WARN", "ERROR")

def analyze_log_file(path: str) -> Tuple[dict, List[tuple]]:
    counts = Counter()
    error_messages = Counter()
    level_re = re.compile(r'\b(INFO|WARN|ERROR)\b')
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = level_re.search(line)
            if m:
                level = m.group(1)
                counts[level] += 1
                if level == "ERROR":
                    # naive error message extract: text after ERROR
                    parts = line.split("ERROR", 1)
                    msg = parts[1].strip() if len(parts) > 1 else line.strip()
                    error_messages[msg] += 1
    top5_errors = error_messages.most_common(5)
    return dict(counts), top5_errors

if __name__ == "__main__":
    counts, top5 = analyze_log_file("sample_logs/system.log")
    print("Counts:", counts)
    print("Top 5 errors:")
    for msg, c in top5:
        print(c, msg)
