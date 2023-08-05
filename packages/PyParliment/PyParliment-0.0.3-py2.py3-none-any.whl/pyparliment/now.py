import requests
import json
from datetime import datetime, timedelta
from tqdm.auto import trange


def get_current(annunciator="CommonsMain"):
    end_point = "Message/message/" + annunciator + "/current"
    baseURL = "https://now-api.parliament.uk/api/"
    url = baseURL + end_point
    response = requests.request("GET", url)
    json_response = json.loads(response.text)

    return json_response


def get_by_datetime(date, annunciator="CommonsMain"):
    if type(date) not in [datetime, str]:
        raise ValueError("parameter 'date' must be of type datetime.datetime or string")
    elif type(date) == str:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    end_point = (
        "Message/message/" + annunciator + "/" + date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    )
    baseURL = "https://now-api.parliament.uk/api/"
    url = baseURL + end_point
    print(url)
    response = requests.request("GET", url)
    json_response = json.loads(response.text)

    return json_response


def get_between_datetime(date_start, date_end, annunciator="CommonsMain"):
    start = datetime.strptime(date_start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(date_end, "%Y-%m-%dT%H:%M:%S.%fZ")
    diff = end - start

    added_ids = []
    slides = []

    for i in trange(0, int(diff.total_seconds() / 60) + 1):
        time = start + timedelta(minutes=i)
        current = get_by_datetime(time)
        # output = "testing/" + str(current["id"]) + ".json"

        for slide in current["slides"]:
            if (current["id"] not in added_ids) and (slide["soundToPlay"] == 1):
                added_ids.append(current["id"])
                slides.append(current)

    return slides
