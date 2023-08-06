import requests

from elvia.error import InvalidRequestBody, AuthError, UnexpectedError
from elvia.types.max_hours_types import MaxHoursParams, MaxHoursResponse
from elvia.types.meter_value_types import MeterValueParams, MeterValueResponse
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse


class MeterValue:
    """
    Elvia MeterValue client

    Contains methods to interact with the MeterValueApi
    """

    def __init__(
        self,
        api_url,
        token,
    ):
        self.api_url = api_url
        self.token = token

    def get_max_hours(self, params: MaxHoursParams) -> MaxHoursResponse:
        """
        Get the hour for maximum consumption (or production)
        in the current and previous month.
        The calculation works on a volume time series than start
        at the 1st of the previous month and ends at the the current hour.

        The calculation uses Norwegian time, even if the input time is UTC.

        :calculate_time: Format - date-time (as date-time in RFC3339). Timestamp for when the max hour calculation should be done. This means the API will pretend to be at this timestamp when calculating. I.e. 2021-09-01T14:59:59+02:00. The value can at most be 3 years back in time. Default: Now (Norwegian time)
        :metering_point_ids - A comma separated list of meteringpointid's. If blank, value is fetched from the contracts related to the access token.
        :include_production - Indicates production or consumption. False = consumption Default: false.
        :return: metering points
        """
        url_base = f"{self.api_url}/customer/metervalues/api/v1/maxhours"

        query = {}
        if "calculate_time" in params:
            query["calculateTime"] = params["calculate_time"]
        if "metering_point_ids" in params:
            query["meteringPointIds"] = ",".join(params["metering_point_ids"])
        if "include_production" in params:
            query["includeProduction"] = (
                "true" if params["include_production"] else "false"
            )
        url = urlparse(url_base)._replace(query=urlencode(query))

        response = requests.get(
            urlunparse(url),
            headers=(
                {
                    "Authorization": "Bearer " + self.token,
                }
            ),
        )
        _verify_response(response, 200)
        return response.json()

    def get_meter_values(self, params: MeterValueParams) -> MeterValueResponse:
        """
        Get metering volumes for the given metering points in the requested period.

        :start_time: Format - date-time (as date-time in RFC3339). From timestamp for consumption. I.e. 2021-09-01T00:00:00+02:00. This value can maximum be 3 years back in time. Default: Last midnight (Norwegian time)
        :end_time: Format - date-time (as date-time in RFC3339). To timestamp for consumption. I.e. 2021-09-02T00:00:00+02:00 The start-end time span can be maximum 1 year. Default: The last hour (Norwegian time)
        :metering_point_ids - A comma separated list of meteringpointid's. If blank, value is fetched from the contracts related to the access token.
        :include_production - Indicates production or consumption. False = consumption Default: false.
        :return: metering points
        """

        url_base = f"{self.api_url}/customer/metervalues/api/v1/metervalues"
        query = {}
        if "start_time" in params:
            query["startTime"] = params["start_time"]
        if "end_time" in params:
            query["endTime"] = params["end_time"]
        if "metering_point_ids" in params:
            query["meteringPointIds"] = ",".join(params["metering_point_ids"])
        if "include_production" in params:
            query["includeProduction"] = (
                "true" if params["include_production"] else "false"
            )
        url = urlparse(url_base)._replace(query=urlencode(query))
        response = requests.get(
            urlunparse(url),
            headers=(
                {
                    "Authorization": "Bearer " + self.token,
                }
            ),
        )
        _verify_response(response, 200)
        return response.json()


def _verify_response(response, expected_status_code):
    if response.status_code == 400:
        raise InvalidRequestBody(
            "Body is malformed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )

    if response.status_code in [401, 403]:
        raise AuthError(
            "Auth failed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )

    if response.status_code != expected_status_code:
        raise UnexpectedError(
            "Received unexpected server response",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )
