"""
This module defines one record for a gas transaction
"""


class GazPoint():

    def __init__(self, date_stamp, liters, price, location=None):
        self.date = date_stamp
        self.liters = liters
        self.price = price
        self.location = location

    def __str__(self):
        return "{}  --->  {}$\n\tliters: {}\n\tprice: {}".format(self.date.isoformat(),
                                                                 self.get_money_spent(),
                                                                 self.liters,
                                                                 self.price)

    def get_money_spent(self):
        return round(self.liters * self.price, 2)

    def get_date(self):
        return self.date


def get_date_from_obj(obj):
    return obj.get_date()


class GazPointData():

    def __init__(self, gaz_point_list):
        self.is_sorted = False
        self.data_points = gaz_point_list

    def __iter__(self):
        return iter(self.data_points)

    def __getitem__(self, key):
        return self.data_points[key]

    def add_point(self, date_stamp, liters, price, location=None):
        self.is_sorted = False
        self.data_points.append(GazPoint(date_stamp, liters, price, location))

    def remove_point(self, index):
        self.data_points.pop(index)

    def list_points(self):
        # change to __str__

        i = 0

        for datum in self.data_points:
            print("({}) {}".format(i, datum))
            i += 1

    def sort_by_date(self):
        if not self.is_sorted:
            self.data_points = sorted(self.data_points, key=get_date_from_obj)
            self.is_sorted = True
