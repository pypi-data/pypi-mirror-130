from pydantic import Field
from pydantic_schemaorg.Thing import Thing
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Organization import Organization
from pydantic_schemaorg.Audience import Audience
from pydantic_schemaorg.Person import Person
from pydantic_schemaorg.InteractAction import InteractAction


class CommunicateAction(InteractAction):
    """The act of conveying information to another person via a communication medium (instrument)"
     "such as speech, email, or telephone conversation.

    See https://schema.org/CommunicateAction.

    """
    type_: str = Field("CommunicateAction", const=True, alias='@type')
    about: Optional[Union[List[Thing], Thing]] = Field(
        None,
        description="The subject matter of the content.",
    )
    language: Any = Field(
        None,
        description="A sub property of instrument. The language used on this action.",
    )
    recipient: Union[List[Union[Organization, Audience, Person, Any]], Union[Organization, Audience, Person, Any]] = Field(
        None,
        description="A sub property of participant. The participant who is at the receiving end of the action.",
    )
    inLanguage: Union[List[Union[str, Any]], Union[str, Any]] = Field(
        None,
        description="The language of the content or performance or used in an action. Please use one of the language"
     "codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also"
     "[[availableLanguage]].",
    )
    

CommunicateAction.update_forward_refs()
