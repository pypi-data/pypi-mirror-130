from elvia.meter_value import MeterValue


class Elvia:
    def __init__(
        self,
        token,
        api_url="https://elvia.azure-api.net",
    ):
        self.token = token
        self.api_url = api_url
        self.meter = None

    def meter_value(self):
        if self.meter is None:
            self.meter = MeterValue(
                self.api_url,
                self.token,
            )
        return self.meter
