from pydantic import Field
from pydantic_schemaorg.Vessel import Vessel
from typing import Any, Optional, Union, List
from pydantic_schemaorg.AnatomicalStructure import AnatomicalStructure


class LymphaticVessel(Vessel):
    """A type of blood vessel that specifically carries lymph fluid unidirectionally toward"
     "the heart.

    See https://schema.org/LymphaticVessel.

    """
    type_: str = Field("LymphaticVessel", const=True, alias='@type')
    originatesFrom: Optional[Union[List[Vessel], Vessel]] = Field(
        None,
        description="The vasculature the lymphatic structure originates, or afferents, from.",
    )
    runsTo: Optional[Union[List[Vessel], Vessel]] = Field(
        None,
        description="The vasculature the lymphatic structure runs, or efferents, to.",
    )
    regionDrained: Union[List[Union[AnatomicalStructure, Any]], Union[AnatomicalStructure, Any]] = Field(
        None,
        description="The anatomical or organ system drained by this vessel; generally refers to a specific"
     "part of an organ.",
    )
    

LymphaticVessel.update_forward_refs()
