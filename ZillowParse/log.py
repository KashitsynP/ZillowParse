import json

def saveData(path:str, mode:str, list):
    with open(path, mode, encoding='utf-8') as file:
        json.dump(list, file)
        print(f'File {path} was sucсessfully saved!')

def loadData(path:str):
    with open(path, 'r') as file:
        obj = json.load(file)
        print(f'File {path} was successfully loaded!')
    return obj