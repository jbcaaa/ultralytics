import json
import os


def get_from_json(jsonpath:str) -> set:
    with open(jsonpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    ret = set()
    for a in data["shapes"]:
        ret.add(a["label"])
    return ret

def main():
    dirs = os.listdir('pre_datasets\labels')
    result = set()
    for dir in dirs:
        print(dir)
        resss = get_from_json(os.path.join('pre_datasets\labels', dir))
        for ress in resss:
            result.add(ress)
    result = list(result)
    for a in range(len(result)):
        result[a] = result[a] + '\n'
    result.sort()
    with open('classes.txt', 'a+', encoding='utf-8') as f:
        f.truncate(0)
        f.writelines(result)
    print('Success!')

if __name__ == '__main__':
    main()