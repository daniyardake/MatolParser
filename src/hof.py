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
                year, grade, name, score, award, region = row
                if (name not in results.keys()):
                    for existing_name in results.keys():
                        if (self.similar(name, existing_name)):
                            name = existing_name
                if (name not in results.keys()):
                    results[name] = {
                        'perfomance': [0, 0, 0, 0],
                        'competitions': [],
                        'region': region
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

    def calc_rating(self, data):
        return 1000*data['perfomance'][0]+100*data['perfomance'][1]+10*data['perfomance'][2]+data['perfomance'][3]

    def competitions_range(self, data):
        comps = [e[0] for e in data['competitions']]
        rng = '{}-{}'.format(min(comps), max(comps))
        return rng

    def run(self):
        inp = self.inp
        out = self.out
        results = self.get_table(inp)
        with open(out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Rank', 'Name', 'Region/School', 'Years', 'Gold', 'Silver', 'Bronze', 'None', 'Total'])
            sorted_tuples = sorted(
                results.items(), key=lambda x: x[1]['perfomance'], reverse=True)
            sorted_results = {k: v for k, v in sorted_tuples}

            queue = []
            prev_score = self.calc_rating(sorted_tuples[0][1])

            for i, (name, data) in enumerate(sorted_results.items(), 1):
                to_write = [
                    name,
                    data['region'],
                    self.competitions_range(data),
                    data['perfomance'][0],
                    data['perfomance'][1],
                    data['perfomance'][2],
                    data['perfomance'][3],
                    data['perfomance'][0] + data['perfomance'][1] +
                    data['perfomance'][2] + data['perfomance'][3]
                ]
                curr_score = self.calc_rating(data)
                if (curr_score != prev_score):
                    num_equals = len(queue)
                    if (len(queue) == 1):
                        writer.writerow(['{}'.format(i-1)] + queue[0])
                    else:
                        rank = '{}-{}'.format(i-num_equals, i-1)
                        for q in queue:
                            writer.writerow([rank] + q)
                    prev_score = curr_score
                    queue = []

                queue.append(to_write)


def main():
    hof = Hof('db.csv', 'hof.csv')
    hof.run()


if __name__ == '__main__':
    main()
