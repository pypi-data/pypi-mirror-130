from pydantic import Field
from pydantic_schemaorg.CoverArt import CoverArt
from pydantic_schemaorg.ComicStory import ComicStory


class ComicCoverArt(CoverArt, ComicStory):
    """The artwork on the cover of a comic.

    See https://schema.org/ComicCoverArt.

    """
    type_: str = Field("ComicCoverArt", const=True, alias='@type')
    

ComicCoverArt.update_forward_refs()
