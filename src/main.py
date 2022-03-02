import pandas as pd
from hof import Hof
from matol_parser import MatolParser


def main():
    data = {
        'website': 'http://matol.kz/',
        'all_results': 'db.csv',
        'hof': 'HallOfFame.csv',
        'web': 'knmo.html'
    }

    parser = MatolParser(data['website'])
    parser.run(data['all_results'])
    print('Results collected')

    hof = Hof(data['all_results'], data['hof'])
    hof.run()
    print('Results processed')

    file = pd.read_csv(data['hof'])
    file.to_html(data['web'])
    print('Web Page Generated')


if __name__ == '__main__':
    main()
