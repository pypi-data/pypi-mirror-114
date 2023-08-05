import requests
from pyparliment import baseURL
from pandas import json_normalize
import json


def register(search, includeDeleted=False, raw=False):
    end_point = "LordsInterests/Register"

    url = (
        baseURL
        + end_point
        + "?searchTerm="
        + search
        + "&includeDeleted="
        + str(includeDeleted)
    )

    response = requests.request("GET", url)

    data = json_normalize(json.loads(response.text)["items"])

    data.drop(
        [
            "links",
            "value.member.nameListAs",
            "value.member.nameDisplayAs",
            "value.member.nameAddressAs",
            "value.member.latestParty.id",
            "value.member.latestParty.abbreviation",
            "value.member.latestParty.backgroundColour",
            "value.member.latestHouseMembership.membershipEndReason",
            "value.member.latestHouseMembership.membershipEndReasonNotes",
            "value.member.latestHouseMembership.membershipEndReasonId",
            "value.member.latestHouseMembership.membershipStatus.statusIsActive",
            "value.member.latestHouseMembership.membershipStatus.statusDescription",
            "value.member.latestHouseMembership.membershipStatus.statusNotes",
            "value.member.latestHouseMembership.membershipStatus.statusId",
            "value.member.thumbnailUrl",
            "value.member.latestParty.foregroundColour",
            "value.member.latestParty.isLordsMainParty",
            "value.member.latestParty.isLordsSpiritualParty",
            "value.member.latestParty.governmentType",
            "value.member.latestParty.isIndependentParty",
            "value.member.latestHouseMembership.membershipFromId",
            "value.member.latestHouseMembership.house",
            "value.member.latestHouseMembership.membershipStatus.statusStartDate",
            "value.member.latestHouseMembership.membershipEndDate",
        ],
        inplace=True,
        axis=1,
    )

    if raw:
        return json.loads(response.text)
    else:
        return data
