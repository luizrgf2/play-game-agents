from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages


class PrintGameState(TypedDict):
    image_base_64: str=None
    messages: Annotated[list, add_messages]
    way_to_run: list=[]

