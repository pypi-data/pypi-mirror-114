import requests
from pyparliment import baseURL
import json
from shapely.geometry import shape


def all_by_id(id_number, accept_old=False):
    end_point = "Location/Constituency/"

    url = baseURL + end_point + str(id_number)

    response = requests.request("GET", url)

    json_response = json.loads(response.text)["value"]

    if json_response["endDate"] is None or accept_old:
        return json_response
    else:
        raise ExtinctConstituincy


def synopsis_by_id(id_number):
    end_point = "Location/Constituency/"

    url = baseURL + end_point + str(id_number) + "/Synopsis"

    response = requests.request("GET", url)

    json_response = json.loads(response.text)["value"]

    return json_response


def representation_by_id(id_number):
    end_point = "Location/Constituency/"

    url = baseURL + end_point + str(id_number) + "/Representations"

    response = requests.request("GET", url)

    json_response = json.loads(response.text)["value"]

    return json_response


def geometry_by_id(id_number):

    end_point = "Location/Constituency/"

    url = baseURL + end_point + str(id_number) + "/Geometry"

    response = requests.request("GET", url)

    json_response = json.loads(json.loads(response.text)["value"])

    if json_response["type"] == "Polygon":
        area = shape(json_response)
    elif json_response["type"] == "MultiPolygon":
        area = shape(json_response)
    else:
        area = 0

    return area


class ExtinctConstituincy(Exception):
    """Raised when the specified constituincy no longer exists"""

    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__("The requested constituincy is no longer in use")
