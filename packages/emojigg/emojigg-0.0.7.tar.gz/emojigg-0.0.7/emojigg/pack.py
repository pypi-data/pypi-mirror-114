class Pack:
    def __init__(
        self,
        data: dict
    ) -> None:
        self._raw = data
        self.id = data.pop('id')
        self.name = data.pop('name')
        self.description = data.pop('description')
        self.slug = data.pop('slug')
        self.image = data.pop('image')
        self.emojis = data.pop('emojis')
        self.download = data.pop('download')
        self.amount = data.pop('amount')
        
    