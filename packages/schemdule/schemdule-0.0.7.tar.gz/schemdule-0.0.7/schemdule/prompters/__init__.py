from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Optional
from enum import Enum


class PromptResult(Enum):
    Empty = 0
    Unsupported = 1     # Unsupported, skip this and go next
    Resolved = 2        # Resolved, go next
    Finished = 3        # Resolved, stop going next
    Failed = 4          # Failed, stop going next


class Prompter(ABC):
    def __init__(self, final: bool = False) -> None:
        self.final = final

    def success(self) -> PromptResult:
        return PromptResult.Finished if self.final else PromptResult.Resolved

    @abstractmethod
    def prompt(self, message: str, payload: Any) -> Any:
        pass

    def __repr__(self) -> str:
        return type(self).__name__


class PrompterHub(Prompter, ABC):
    @abstractmethod
    def register(self, prompter: Prompter) -> None:
        pass


class PrompterPayload(ABC):
    pass


class PrompterPayloadCollection(PrompterPayload):
    def __init__(self, payloads: Optional[List[Any]]) -> None:
        self.payloads = payloads if payloads is not None else []

    def try_get(self, type: type) -> Iterable[Any]:
        for item in self.payloads:
            if isinstance(item, type):
                yield item
