from typing_extensions import TypedDict
from typing import List

from elvia.types.common import CustomerContract


class MeterValueParams(TypedDict):
    start_time: str
    end_time: str
    metering_point_ids: List[str]
    include_production: bool


class MeterValueTimeSeries(TypedDict):
    startTime: str
    endTime: str
    value: float
    uom: str
    production: bool
    verified: bool


class MeterValueDetails(TypedDict):
    fromHour: str
    toHour: str
    resolutionMinutes: int
    timeSeries: List[MeterValueTimeSeries]


class MeterValueMeteringPoint(TypedDict):
    meteringPointId: str
    customerContract: CustomerContract
    metervalue: MeterValueDetails


class MeterValueResponse(TypedDict):
    meteringpoints: List[MeterValueMeteringPoint]
