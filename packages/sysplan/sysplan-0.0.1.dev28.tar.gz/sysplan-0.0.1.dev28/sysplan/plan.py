import copy


class Plan(dict):
    def __init__(self, root, config, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.name = name
        self.config = config

    async def write(self):
        pass

    async def activate(self):
        pass

    async def diff(self):
        pass

    async def destroy(self):
        pass

    def plans(self):
        return [copy.deepcopy(self)]
