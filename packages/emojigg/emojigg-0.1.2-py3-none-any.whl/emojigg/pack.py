
from typing import List

class Pack:
    def __init__(
        self,
        state,
        data: dict
    ) -> None:
        self._state = state
        self._raw = data
        
        self.id: int = data.pop('id')
        self.name: str = data.pop('name')
        self.description: str = data.pop('description')
        self.slug: str = data.pop('slug')
        self.image: str = data.pop('image')
        self.url: str = self.image
        self.raw_emojis: List[str] = data.pop('emojis')
        self.amount: int = data.pop('amount')
    
    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def formatted_name(self) -> str:
        """
        Returns
        -------
        str
            The pack's name formatted correctly with caps.
        """
        return self.name.capitalize()

    @property
    def formatted_description(self) -> str:
        """
        Returns
        -------
        str
            The pack's description formatted correctly with caps.
        """
        return self.description.capitalize()

    async def emojis(self):
        """
        A coro that turns the raw emoji list to a list of Emoji objects.

        This doesn't work MOST of the time because the API doesn't fetch all emojis at once.

        Returns
        -------
        Optional[List[Emoji]]
        """
        final_emojis = []
        formatted_emojis = [emoji[0: len(emoji)-4] for emoji in self.raw_emojis]
        emojis = await self._state.fetch_emojis()
        for emoji in emojis:
            if emoji.slug in formatted_emojis:
                final_emojis.append(emoji)
        print(final_emojis or "NO emojis.")
        return final_emojis
            
    
    