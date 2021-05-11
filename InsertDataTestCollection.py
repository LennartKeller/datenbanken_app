import json

if __name__ == '__main__':
    with open("TestCollection.json", "r") as in_file:
        data = json.load(in_file)
    with open("20ng.txt") as data_file:
        data['Texts'] = []
        for idx, line in enumerate(data_file):
            data['Textsi'].append(" ".join(line.split()))
            if idx == 99:
                break
    with open("TestCollection.json", "w") as out_file:
        json.dump(data, out_file, indent=4)
