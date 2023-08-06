from typing_extensions import TypedDict
from typing import List

from elvia.types.common import CustomerContract


class MaxHoursParams(TypedDict):
    calculate_time: str
    metering_point_ids: List[str]
    include_production: bool


class MaxHoursParams(TypedDict):
    start_time: str
    end_time: str
    metering_point_ids: List[str]
    include_production: bool


class MaxHoursTimeSeries(TypedDict):
    startTime: str
    endTime: str
    value: float
    uom: str
    noOfMonthsBack: int
    production: bool
    verified: bool


class MaxHoursMeteringPoint(TypedDict):
    meteringPointId: str
    customerContract: CustomerContract
    maxHoursCalculatedTime: str
    maxHoursFromTime: str
    maxHoursToTime: str
    maxHours: List[MaxHoursTimeSeries]


class MaxHoursResponse(TypedDict):
    meteringpoints: List[MaxHoursMeteringPoint]
