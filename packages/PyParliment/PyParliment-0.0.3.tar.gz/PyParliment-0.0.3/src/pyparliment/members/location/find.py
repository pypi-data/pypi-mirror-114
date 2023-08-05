import requests
from pyparliment import baseURL
import pandas as pd
from pandas import json_normalize
import json
from math import ceil
import pyparliment.members.location.constituincy as constituincy
from tqdm.auto import tqdm

tqdm.pandas()


def search(search):

    skip = 0
    take = 20

    end_point = "Location/Constituency/Search"

    url = (
        baseURL
        + end_point
        + "?searchText="
        + search
        + "&skip="
        + str(skip)
        + "&take="
        + str(take)
    )

    response = requests.request("GET", url)

    json_response = json.loads(response.text)

    results = json_response["totalResults"]

    number_of_requests = ceil(results / take)

    data = []

    for i in range(0, number_of_requests):
        url = (
            baseURL
            + end_point
            + "?searchText="
            + search
            + "&skip="
            + str(skip)
            + "&take="
            + str(take)
        )

        response = requests.request("GET", url)

        json_response = json.loads(response.text)

        data.append(json_normalize(json_response["items"]))

        skip = skip + take

    data = pd.concat(data)

    data.drop(
        [
            "links",  # noqa: E501
            "value.startDate",  # noqa: E501
            "value.currentRepresentation.member.value.nameListAs",  # noqa: E501
            "value.currentRepresentation.member.value.nameDisplayAs",  # noqa: E501
            "value.currentRepresentation.member.value.nameFullTitle",  # noqa: E501
            "value.currentRepresentation.member.links",  # noqa: E501
            "value.currentRepresentation.representation.membershipFrom",  # noqa: E501
            "value.currentRepresentation.representation.membershipFromId",  # noqa: E501
            "value.currentRepresentation.representation.house",  # noqa: E501
            "value.endDate",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.id",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.name",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.backgroundColour",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.foregroundColour",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipStatus.statusNotes",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipStatus.statusId",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipStatus.statusStartDate",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.isLordsMainParty",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.isLordsSpiritualParty",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.governmentType",  # noqa: E501
            "value.currentRepresentation.member.value.latestParty.isIndependentParty",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipEndReasonId",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipStatus.statusIsActive",  # noqa: E501
            "value.currentRepresentation.representation.membershipEndDate",  # noqa: E501
            "value.currentRepresentation.representation.membershipEndReason",  # noqa: E501
            "value.currentRepresentation.representation.membershipEndReasonNotes",  # noqa: E501
            "value.currentRepresentation.representation.membershipEndReasonId",  # noqa: E501
            "value.currentRepresentation.representation.membershipStatus",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipFrom",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipFromId",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.house",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipEndDate",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipStartDate",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipEndReason",  # noqa: E501
            "value.currentRepresentation.member.value.latestHouseMembership.membershipEndReasonNotes",  # noqa: E501
            "value.currentRepresentation.member.value.thumbnailUrl",  # noqa: E501
        ],
        inplace=True,
        axis=1,
    )

    if "value.currentRepresentation" in data.columns:
        data.drop(["value.currentRepresentation"], inplace=True, axis=1)
    data.columns = [
        "Constituincy ID",
        "Constituincy Name",
        "Member ID",
        "Member Name",
        "Party",
        "Gender",
        "Status",
        "Start date",
    ]

    data.reset_index(inplace=True, drop=True)

    shapes = data.progress_apply(
        lambda row: constituincy.geometry_by_id(row["Constituincy ID"]), axis=1
    )

    data["shapes"] = shapes

    return data
