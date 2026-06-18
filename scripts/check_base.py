"""
Контрольная проверка базы (этап 2 УИИ).
Прогоняет по всем JSON в data/prepared/ и считает проблемные реплики.
 
Запуск из корня проекта:  python scripts/check_base.py
"""
 
import json
import glob
import re
 
PREPARED_DIR = "data/prepared/*.json"
 
 
def check_base():
    files = sorted(glob.glob(PREPARED_DIR))
    if not files:
        print("Не найдено JSON в data/prepared/ — проверь путь и что парсер отработал.")
        return
 
    total = 0
    glued_dash = []     # внутриблочный дефис: "?- ", ".- ", "!- " — слиплись говорящие
    double_space = []   # двойные пробелы (остаток от join/чистки)
    empty = []          # пустые/из пробелов
    per_file = []       # сколько реплик в каждом файле
 
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        per_file.append((fp.split("/")[-1].split("\\")[-1], len(data)))
        total += len(data)
        for r in data:
            t = r["text"]
            if re.search(r"[.!?]\s?-\s", t):     # знак конца + дефис-разделитель
                glued_dash.append((fp, t))
            if "  " in t:                         # двойной пробел
                double_space.append((fp, t))
            if not t.strip():                     # пусто
                empty.append((fp, t))
 
    print("=" * 60)
    print(f"ВСЕГО РЕПЛИК: {total}  (файлов: {len(files)})")
    print("=" * 60)
 
    print("\nПо файлам:")
    for name, n in per_file:
        print(f"  {name:<16} {n}")
 
    print(f"\n[1] Внутриблочный дефис (слиплись говорящие): {len(glued_dash)}")
    for fp, t in glued_dash[:10]:
        name = fp.split("/")[-1].split("\\")[-1]
        print(f"    [{name}] {t[:90]}")
 
    print(f"\n[2] Двойные пробелы: {len(double_space)}")
    for fp, t in double_space[:10]:
        name = fp.split("/")[-1].split("\\")[-1]
        print(f"    [{name}] {t[:90]}")
 
    print(f"\n[3] Пустые реплики: {len(empty)}")
 
    print("\n" + "=" * 60)
    print("Для сдачи: впиши TOTAL и числа дефектов [1]/[2]/[3].")
    print("Если [1] большое — чиним дефис построчно. Если единицы — отмечаем и сдаём.")
    print("=" * 60)
 
 
if __name__ == "__main__":
    check_base()