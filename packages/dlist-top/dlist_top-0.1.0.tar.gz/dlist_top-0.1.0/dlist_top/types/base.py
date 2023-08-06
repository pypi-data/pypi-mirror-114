from types import SimpleNamespace
from typing import Any

class Base(SimpleNamespace):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        for k, Type in self.__annotations__.items():
            if Type is Any or Type is None: continue

            old = self.__dict__[k] \
                if k in self.__dict__ \
                else None

            try:
                try:
                    self.__dict__[k] = Type.parse(old)
                except AttributeError:
                    self.__dict__[k] = Type(old)

            except Exception as err:
                raise type(err)(f'cannot {k} to type {Type}: {err}') from None