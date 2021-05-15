import json

if __name__ == '__main__':
    with open("IMDBCollection.json", "r") as in_file:
        data = json.load(in_file)
    with open("imdb_reviews.txt") as data_file:
        data['Texts'] = []
        for idx, line in enumerate(data_file):
            data['Texts'].append(" ".join(line.split()))
    with open("LargeIMDBCollection.json", "w") as out_file:
        json.dump(data, out_file, indent=4)
