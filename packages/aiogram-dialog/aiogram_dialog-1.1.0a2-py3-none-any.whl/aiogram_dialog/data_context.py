from typing import Dict, Awaitable, Callable, List

DataGetter = Callable[..., Awaitable[Dict]]


class CompositeGetter:
    def __init__(self, *getters: DataGetter):
        self.getters: List[DataGetter] = list(getters)

    def __call__(self, *args, **kwargs):
        data = {}
        for g in self.getters:
            data.update(await g(**kwargs))
        return data
