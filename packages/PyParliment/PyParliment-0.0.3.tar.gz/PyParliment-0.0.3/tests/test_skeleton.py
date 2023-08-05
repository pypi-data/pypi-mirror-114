# print(help("modules"))

from pyparliment.members.location import find
from pyparliment import now
from datetime import datetime
import pytest

__author__ = "George Sykes"
__copyright__ = "George Sykes"
__license__ = "MIT"


def test_find():
    """API Tests"""
    test_data = find.search("")
    assert "int64" not in test_data.dtypes
    assert len(test_data) == 650


def test_now_get_current():
    """API Tests"""
    out = now.get_current()
    assert type(out) == dict
    assert list(out.keys()) == [
        "id",
        "slides",
        "scrollingMessages",
        "annunciatorType",
        "publishTime",
        "isSecurityOverride",
        "showCommonsBell",
        "showLordsBell",
    ]


def test_now_get_by_datetime():
    assert type(now.get_by_datetime(datetime.now())) == dict

    for i in ["CommonsMain", "LordsMain"]:
        assert type(now.get_by_datetime(datetime.now(), annunciator=i)) == dict, (
            "Failed different anunciators the output was not a dictionary for " + i
        )

    assert (
        type(now.get_by_datetime("2020-06-01T13:02:12.956Z")) == dict
    ), "Failed getting by datetime from a string datetime"
    with pytest.raises(ValueError):
        now.get_by_datetime("2020-06-01")
