from pydantic import Field
from pydantic_schemaorg.AnatomicalStructure import AnatomicalStructure
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Vessel import Vessel


class Vein(Vessel):
    """A type of blood vessel that specifically carries blood to the heart.

    See https://schema.org/Vein.

    """
    type_: str = Field("Vein", const=True, alias='@type')
    tributary: Optional[Union[List[AnatomicalStructure], AnatomicalStructure]] = Field(
        None,
        description="The anatomical or organ system that the vein flows into; a larger structure that the vein"
     "connects to.",
    )
    drainsTo: Any = Field(
        None,
        description="The vasculature that the vein drains into.",
    )
    regionDrained: Union[List[Union[AnatomicalStructure, Any]], Union[AnatomicalStructure, Any]] = Field(
        None,
        description="The anatomical or organ system drained by this vessel; generally refers to a specific"
     "part of an organ.",
    )
    

Vein.update_forward_refs()
