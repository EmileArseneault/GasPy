"""
This module provides a command line interface for working with the data
"""
import time

from datetime import date
from json_parser import GazPointStorageJson
from gaz_point import GazPointData
from statistics import Statistics
from visualisation import Visualisation


class Menu():

    menu_string = """
----  Menu  ----
add [date] [liters] [price] [location]
list
remove [index]
show [hist]
sort
stats [start_date] [end_date]
help
exit
"""

    def __init__(self):

        # Load data
        parse_start = time.perf_counter_ns()
        self.storage = GazPointStorageJson("data.json")
        parse_end = time.perf_counter_ns()

        load_start = time.perf_counter_ns()
        self.gaz_data = GazPointData(self.storage.load_gaz_points())
        load_end = time.perf_counter_ns()

        stats_start = time.perf_counter_ns()
        self.statistics = Statistics(self.gaz_data)
        self.viz = Visualisation()
        stats_end = time.perf_counter_ns()

        print("Json parsing time : {}".format(parse_end-parse_start))
        print("Data loading time : {}".format(load_end-load_start))
        print("Stats loading time : {}".format(stats_end-stats_start))

    def start(self):

        answer = "help"

        while (answer != "exit") and (answer != "quit"):

            answer = answer.split()

            if answer[0] == "help":
                print(Menu.menu_string)
            elif answer[0] == "add":
                if len(answer) == 5:
                    self.gaz_data.add_point(date.fromisoformat(answer[1]),
                                            float(answer[2]),
                                            float(answer[3]),
                                            answer[4])
                    print(self.gaz_data[-1])
                elif len(answer) == 4:
                    self.gaz_data.add_point(date.fromisoformat(answer[1]),
                                            float(answer[2]),
                                            float(answer[3]))
                    print(self.gaz_data[-1])
                else:
                    print()
                    print("add doesn't have correct amount of parameters")
                    print()
                    print(Menu.menu_string)
            elif answer[0] == "list":
                self.gaz_data.list_points()
            elif answer[0] == "remove":
                if len(answer) == 2:
                    self.gaz_data.remove_point(int(answer[1]))
                else:
                    print()
                    print("add doesn't have correct amount of parameters")
                    print()
                    print(Menu.menu_string)
            elif answer[0] == "show":
                self.viz.load_data(self.gaz_data.data_points)
                self.viz.generate_plot()
                print("Show data")
            elif answer[0] == "sort":
                self.gaz_data.sort_by_date()
                print("Data is sorted")
            elif answer[0] == "stats":
                if len(answer) == 1:
                    (months, money) = self.statistics.calculate_spent_per_month()
                    mean = self.statistics.calculate_spent_months_mean()
                elif len(answer) == 2:
                    (months, money) = self.statistics.calculate_spent_per_month(date.fromisoformat(answer[1]))
                    mean = self.statistics.calculate_spent_months_mean(date.fromisoformat(answer[1]))
                elif len(answer) == 3:
                    (months, money) = self.statistics.calculate_spent_per_month(
                            date.fromisoformat(answer[1]), date.fromisoformat(answer[2]))
                    mean = self.statistics.calculate_spent_months_mean(
                            date.fromisoformat(answer[1]), date.fromisoformat(answer[2]))

                print("----  Statistics  ----")
                for month, dolla in zip(months, money):
                    print(" - {}\t{:.2f}$".format(month.isoformat(), dolla))
                print()
                print(
                    "   mean  --->\t{:.2f}$".format(mean))

            else:
                print()
                print("Unknown command")
                print()
                print(Menu.menu_string)

            answer = input("> ").strip()

        # Save data before closing
        self.storage.write_gaz_points(self.gaz_data.data_points)


if __name__ == "__main__":
    init_start = time.perf_counter_ns()
    menu = Menu()
    init_end = time.perf_counter_ns()
    print("Initialization time : {}".format(init_end-init_start))
    menu.start()
