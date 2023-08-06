import io
from typing import (
    Dict,
    Union
)

class Emoji:
    def __init__(
        self, 
        state,
        data: Dict
        ) -> None:
        self._state = state
        
        self._raw: Dict = data
        self.id: int = data.pop('id')
        self.title: str = data.pop('title')
        self.slug: str = data.pop('slug')
        self.image: str = data.pop('image')
        self.url: str = self.image
        self.description: str = data.pop('description')
        self.category: int = data.pop('category')

        license = data.pop('license')
        if license.isdigit():
            license = int(license)
        self.license: Union[int, str] = license
        self.source: str = data.pop('source')
        self.faves: int = data.pop('faves')
        self.submitted_by: str = data.pop('submitted_by')
        self.width: int = data.pop('width')
        self.height: int = data.pop('height')
        self.filesize: int = data.pop('filesize')

    def __str__(self) -> str:
        return self.title
    
    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def formatted_description(self) -> str:
        """
        Returns
        -------
        str
            The emojis description formatted correctly with caps.
        """
        return self.description.capitalize()

    async def to_bytes(self) -> Union[io.BytesIO, None]:
        """
        |coro|
        
        Turn the image url to a bytes like object.
        
        Returns
        -------
            Union[io.BytesIO, None]
        """
        return await self._state.url_to_bytes(self.image)