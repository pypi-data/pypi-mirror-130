from pydantic import Field
from pydantic_schemaorg.BusStation import BusStation
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Trip import Trip


class BusTrip(Trip):
    """A trip on a commercial bus line.

    See https://schema.org/BusTrip.

    """
    type_: str = Field("BusTrip", const=True, alias='@type')
    departureBusStop: Union[List[Union[BusStation, Any]], Union[BusStation, Any]] = Field(
        None,
        description="The stop or station from which the bus departs.",
    )
    arrivalBusStop: Union[List[Union[BusStation, Any]], Union[BusStation, Any]] = Field(
        None,
        description="The stop or station from which the bus arrives.",
    )
    busNumber: Optional[Union[List[str], str]] = Field(
        None,
        description="The unique identifier for the bus.",
    )
    busName: Optional[Union[List[str], str]] = Field(
        None,
        description="The name of the bus (e.g. Bolt Express).",
    )
    

BusTrip.update_forward_refs()
