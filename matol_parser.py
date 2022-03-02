from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import csv


class MatolParser:
    def __init__(self, base_url='http://matol.kz'):
        self.base_url = base_url
        self.year_links = self.get_year_links()
        self.links = self.get_links(self.year_links)

    def get_year_links(self):
        years = urllib.request.urlopen(
            '{}/nodes/13'.format(self.base_url)).read()
        years_soup = BeautifulSoup(years, 'lxml')
        anchors = years_soup.find('table').findAll('a')
        links = [a.get('href') for a in anchors]
        return links

    def get_links(self, links):
        result = []
        for link in links:
            try:
                grades = urllib.request.urlopen(
                    '{}{}'.format(self.base_url, link)).read()
            except HTTPError as e:
                pass

            grades_soup = BeautifulSoup(grades, 'lxml')
            anchors = grades_soup.find('table').findAll('a', style=True)
            for a in anchors:
                result.append(a.get('href'))
        return result

    def get_table(self, link):
        table = pd.read_html('{}{}'.format(self.base_url, link))[0]
        return table.values.tolist()[1:]

    def get_year_grade(self, link):
        competition = urllib.request.urlopen(
            '{}{}'.format(self.base_url, link)).read()
        competition_soup = BeautifulSoup(competition, 'lxml')
        year_grade = [word for word in competition_soup.find(
            'h2').text.split() if word.isnumeric()]
        return year_grade

    def clean_award(self, award):
        if (isinstance(award, float)):
            return ''
        words = award.split()
        if (('I' in words) or ('1' in words)):
            return '1'
        if (('II' in words) or ('2' in words)):
            return '2'
        if (('III' in words) or ('3' in words)):
            return '3'
        return ''

    def save(self, link, db):
        results = self.get_table(link)
        year_grade = self.get_year_grade(link)

        with open(db, 'a') as f:
            csvwriter = csv.writer(f)
            for result in results:
                name = result[1]
                award = self.clean_award(result[-1])
                score = result[-2]
                year = year_grade[0]
                grade = year_grade[1]
                csvwriter.writerow([year, grade, name, score, award])

    def run(self, db):
        for link in self.links:
            self.save(link, db)


def main():
    parser = MatolParser('http://matol.kz/')
    parser.run('db.csv')


if __name__ == '__main__':
    main()
