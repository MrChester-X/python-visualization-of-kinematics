import json

import globals as gb
from point_controller import Point


class FileJSON:
    def __init__(self, path):
        self.path = path

    def get_json(self):
        with open(self.path) as file:
            return json.load(file)

    def set_json(self, data):
        with open(self.path, "w+") as file:
            json.dump(data, file)


class PointsJSON(FileJSON):
    def __init__(self, *args):
        super().__init__(*args)

    def load_points(self):
        data = self.get_json()

        gb.form.points_list.clear()
        gb.points.clear()

        for dt in data.get("points", []):
            gb.form.add_point(
                dt["x"], dt["y"], dt["speed"], dt["alpha"], dt["name"],
                [int(i) for i in dt["color"].split(", ")])

    def save_points(self):
        data = {"points": []}

        for point in gb.points:
            data["points"].append({
                "name": point.get_name(),
                "y": point.get_y(),
                "x": point.get_x(),
                "speed": point.get_speed(),
                "alpha": point.get_alpha(),
                "color": ", ".join([str(i) for i in point.get_color()])
            })

        self.set_json(data)


def load_points():
    points_file = PointsJSON(gb.path_json_points)
    points_file.load_points()


def save_points():
    points_file = PointsJSON(gb.path_json_points)
    points_file.save_points()
