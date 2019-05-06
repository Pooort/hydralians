import csv

class CsvRepo:
    @staticmethod
    def get_codags_and_quantity():

        with open('order.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row['CODAG'], row['Quantité']
