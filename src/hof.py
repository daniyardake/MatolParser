import csv
from difflib import SequenceMatcher


class Hof:
    def __init__(self, inp, out):
        self.inp = inp
        self.out = out

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio() > 0.8

    def get_table(self, db):
        results = {}
        with open('db.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                year, grade, name, score, award = row
                if (name not in results.keys()):
                    for existing_name in results.keys():
                        if (self.similar(name, existing_name)):
                            name = existing_name
                if (name not in results.keys()):
                    results[name] = {
                        'perfomance': [0, 0, 0, 0],
                        'competitions': []
                    }
                if (award == '1'):
                    results[name]['perfomance'][0] += 1
                elif (award == '2'):
                    results[name]['perfomance'][1] += 1
                elif (award == '3'):
                    results[name]['perfomance'][2] += 1
                else:
                    results[name]['perfomance'][3] += 1

                results[name]['competitions'].append(
                    [year, grade, score, award])
        return results

    def run(self):
        inp = self.inp
        out = self.out
        results = self.get_table(inp)
        with open(out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['#', 'Name', 'G', 'S', 'B', 'N'])
            sorted_tuples = sorted(
                results.items(), key=lambda x: x[1]['perfomance'], reverse=True)
            sorted_results = {k: v for k, v in sorted_tuples}
            i = 1
            for name, data in sorted_results.items():
                writer.writerow([i, name, data['perfomance'][0], data['perfomance']
                                [1], data['perfomance'][2], data['perfomance'][3]])
                i += 1


def main():
    hof = Hof('db.csv', 'hof.csv')
    hof.run()


if __name__ == '__main__':
    main()
