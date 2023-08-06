from .categories import Categories

class Emoji:
    def __init__(
        self, 
        data: dict
        ) -> None:
        self._raw = data
        self.id = data.pop('id')
        self.title = data.pop('title')
        self.slug = data.pop('slug')
        self.image = data.pop('image')
        self.description = data.pop('description')
        self.license = data.pop('license')
        self.source = data.pop('source')
        self.faves = data.pop('faves')
        self.submitted_by = data.pop('submitted_by')
        self.width = data.pop('width')
        self.height = data.pop('height')
        self.filesize = data.pop('filesize')
        
    @property
    def formatted_description(self) -> str:
        """
        Returns
        -------
        str
            The emojis description formatted correctly with caps.
        """
        return self.description.capitalize()

    @property
    def category(self) -> str:
        category = self._raw.get('category')
        return Categories().types.get(str(category))