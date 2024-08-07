import pytest
import tenacity
from freezegun import freeze_time

from itou.utils.apis.datadog import DatadogApiClient, DatadogBadResponseException


def test_count_daily_logs(settings, respx_mock):
    settings.API_DATADOG_BASE_URL = "https://un-toutou-nomme-donnee.fr/"
    expected = 11338
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        200,
        json={
            "meta": {
                "elapsed": 192,
                "request_id": "blablabla",
                "status": "done",
            },
            "data": {"buckets": [{"computes": {"c0": expected}, "by": {}}]},
        },
    )
    client = DatadogApiClient()
    result = client.count_daily_logs()
    assert result == expected


def test_count_daily_unique_users(settings, respx_mock):
    settings.API_DATADOG_BASE_URL = "https://un-toutou-nomme-donnee.fr/"
    expected = 12
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        200,
        json={
            "meta": {
                "elapsed": 192,
                "request_id": "blablabla",
                "status": "done",
            },
            "data": {"buckets": [{"computes": {"c0": expected}, "by": {}}]},
        },
    )
    client = DatadogApiClient()
    result = client.count_daily_unique_users()
    assert result == expected


def test_count_daily_unique_ip_addresses(settings, respx_mock):
    settings.API_DATADOG_BASE_URL = "https://un-toutou-nomme-donnee.fr/"
    expected = 12
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        200,
        json={
            "meta": {
                "elapsed": 192,
                "request_id": "blablabla",
                "status": "done",
            },
            "data": {"buckets": [{"computes": {"c0": expected}, "by": {}}]},
        },
    )
    client = DatadogApiClient()
    result = client.count_daily_unique_ip_addresses()
    assert result == expected


def test_no_result(settings, respx_mock):
    settings.API_DATADOG_BASE_URL = "https://un-toutou-nomme-donnee.fr/"
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        200,
        json={
            "meta": {
                "elapsed": 182,
                "request_id": "12345",
                "status": "done",
            },
            "data": {"buckets": []},
        },
    )
    client = DatadogApiClient()
    assert client.count_daily_unique_users() == 0


@freeze_time("2024-06-18")
def test_datadog_exceptions(settings, respx_mock, mocker, caplog):
    settings.API_DATADOG_BASE_URL = "https://un-toutou-nomme-donnee.fr/"
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        200,
        json={
            "meta": {
                "elapsed": 182,
                "request_id": "12345",
                "status": "done",
            },
            "data": {"buckets": [{"computes": {"c100000000": "nothing"}, "by": {}}]},
        },
    )
    client = DatadogApiClient()
    with pytest.raises(DatadogBadResponseException):
        client.count_daily_unique_users()
    assert "DatadogBadResponseException" in caplog.text
    # from and to timestamps are logged when a DatadogBadResponse raises.
    # This is the `from` timestamp.
    assert "1718582400000" in caplog.text

    mocker.patch("tenacity.nap.time.sleep", mocker.MagicMock())
    respx_mock.post("https://un-toutou-nomme-donnee.fr/logs/analytics/aggregate").respond(
        429,
        json={
            "status": "error",
            "code": 429,
            "errors": ["Too many requests"],
            "statuspage": "http://status.datadoghq.eu",
            "twitter": "http://twitter.com/datadogops",
            "email": "support@datadoghq.com",
        },
    )
    client = DatadogApiClient()
    with pytest.raises(tenacity.RetryError):
        client.count_daily_unique_users()
