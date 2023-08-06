from pydantic import StrictBool, Field
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Person import Person
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Event import Event


class PublicationEvent(Event):
    """A PublicationEvent corresponds indifferently to the event of publication for a CreativeWork"
     "of any type e.g. a broadcast event, an on-demand event, a book/journal publication via"
     "a variety of delivery media.

    See https://schema.org/PublicationEvent.

    """
    type_: str = Field("PublicationEvent", const=True, alias='@type')
    publishedBy: Optional[Union[List[Union[Organization, Person]], Union[Organization, Person]]] = Field(
        None,
        description="An agent associated with the publication event.",
    )
    publishedOn: Any = Field(
        None,
        description="A broadcast service associated with the publication event.",
    )
    free: Optional[Union[List[StrictBool], StrictBool]] = Field(
        None,
        description="A flag to signal that the item, event, or place is accessible for free.",
    )
    

PublicationEvent.update_forward_refs()
