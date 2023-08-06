from pydantic import Field
from pydantic_schemaorg.DataFeedItem import DataFeedItem
from pydantic_schemaorg.Thing import Thing
from typing import Any, Optional, Union, List
from pydantic_schemaorg.Dataset import Dataset


class DataFeed(Dataset):
    """A single feed providing structured information about one or more entities or topics.

    See https://schema.org/DataFeed.

    """
    type_: str = Field("DataFeed", const=True, alias='@type')
    dataFeedElement: Optional[Union[List[Union[str, DataFeedItem, Thing]], Union[str, DataFeedItem, Thing]]] = Field(
        None,
        description="An item within in a data feed. Data feeds may have many elements.",
    )
    

DataFeed.update_forward_refs()
