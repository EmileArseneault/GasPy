"""
This module calculates statistics based on the gaz data
"""
from datetime import date


class Statistics():

    def __init__(self, gaz_point_data):
        self.gaz_data = gaz_point_data

    def calculate_spent_per_month(self, start_date=None, end_date=None):

        self.gaz_data.sort_by_date()

        if start_date is None:
            start_date = self.gaz_data[0].get_date()

        if end_date is None:
            end_date = self.gaz_data[-1].get_date()

        months = list()
        spent = list()

        for datum in self.gaz_data:
            
            # Limits to data range selected
            if datum.get_date() < start_date:
                continue
            
            if datum.get_date() > end_date:
                continue

            # Populate the first item in the lists
            if not months:
                months.append(datum.get_date().replace(day=1))
                spent.append(datum.get_money_spent())
                continue

            if datum.get_date().replace(day=1) > months[-1].replace(day=1):
                # Month has changed since last datum
                months.append(datum.get_date().replace(day=1))
                spent.append(datum.get_money_spent())
            else:
                # Datum is in the same month
                spent[-1] = spent[-1] + datum.get_money_spent()

        return (months, spent)

    def calculate_spent_months_mean(self, start_date=None, end_date=None):

        (months, spent) = self.calculate_spent_per_month(start_date, end_date)
        sum = 0

        for dolla in spent:
            sum += dolla

        mean = round(float(sum)/len(months), 2)

        return mean
