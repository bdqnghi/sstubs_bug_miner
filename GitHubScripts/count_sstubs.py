import json
import lizard

if __name__ == "__main__":
    # path = "mined_bug/0/sstubs.json"
    total_bugs = 0
    total_sstubs = []
    for i in range(100):
        # 61, 81 91, 97
        path = f"mined_bug/{i}/sstubs.json"    
        try:
            f = open(path)
            data = json.load(f)
            print(len(data))
            total_bugs = total_bugs + len(data)
            total_sstubs.extend(data)
        except Exception as e:
            print(path)
            print(e)

    print(total_bugs)
    with open('all_sstubs_v1.json', 'w', encoding='utf-8') as f1:
        json.dump(total_sstubs, f1, ensure_ascii=False, indent=4)
    