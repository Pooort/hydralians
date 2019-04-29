import csv

class CsvRepo:
    @staticmethod
    def get_codags():

        with open('data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row['codag']
