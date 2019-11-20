"""
Every record of GazPoint are stored in a json file with this format

[
  {
    "date": "21/01/2019",
    "price": 1.169,
    "liters": 32
  },
  {
    "date": "21/01/2019",
    "price": 1.169,
    "liters": 32
  }
]
"""

import json
from datetime import date
from gaz_point import GazPoint


# Handler method for serializing GazPoint object
def gaz_point_handler(obj):
    if isinstance(obj, GazPoint):
        return {
            "date": obj.date.isoformat(),
            "price": obj.price,
            "liters": obj.liters,
            "location": obj.location,
        }
    else:
        raise Exception("Unknown json object to parse : {}".format(obj))


class GazPointStorageJson():

    def __init__(self, filename):

        filestream = open(filename)

        self.json_object = json.load(filestream)
        self.gaz_point_list = list()
        self.filename = filename

        filestream.close()

        for gaz in self.json_object:
            gaz_date = date.fromisoformat(gaz["date"])
            self.gaz_point_list.append(
                GazPoint(gaz_date, gaz["liters"], gaz["price"], gaz["location"])
            )

    def load_gaz_points(self):
        return self.gaz_point_list

    def write_gaz_points(self, gaz_point_list):
        filestream = open(self.filename, "w")
        json.dump(gaz_point_list, filestream,
                  default=gaz_point_handler, indent=4)
        filestream.close()


if __name__ == "__main__":

    gpp = GazPointStorageJson("data.json")

    gaz_list = gpp.load_gaz_points()
    print(gaz_list)

    gp = GazPoint(date.today(), 23, 1.1789)
    gaz_list.append(gp)
    print(gaz_list)

    gpp.write_gaz_points(gaz_list)
