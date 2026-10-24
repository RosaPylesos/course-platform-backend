from collections import defaultdict
from collections.abc import Callable
from typing import Any



EventHandler = Callable[[Any], None]



class EventDispatcher:
    def __init__(self) -> None:
        self._hanlders: dict[
            type, 
            list[EventHandler]
        ] = defaultdict(list)

    def register(
        self,
        event_type: type,
        handler: EventHandler,
    ) -> None:
        self._hanlders[event_type].append(handler)

    def dispatch(self, event: object) -> None:
        for handler in self._hanlders[type(event)]:
            handler(event)
