from pydantic import Field
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Audience import Audience


class BusinessAudience(Audience):
    """A set of characteristics belonging to businesses, e.g. who compose an item's target"
     "audience.

    See https://schema.org/BusinessAudience.

    """
    type_: str = Field("BusinessAudience", const=True, alias='@type')
    yearsInOperation: Any = Field(
        None,
        description="The age of the business.",
    )
    numberOfEmployees: Any = Field(
        None,
        description="The number of employees in an organization e.g. business.",
    )
    yearlyRevenue: Any = Field(
        None,
        description="The size of the business in annual revenue.",
    )
    

BusinessAudience.update_forward_refs()
