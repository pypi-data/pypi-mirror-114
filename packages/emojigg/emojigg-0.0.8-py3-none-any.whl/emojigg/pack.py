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
        self.emojis: List[str] = data.pop('emojis')  # I want to change this.
        self.amount: int = data.pop('amount')
    
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
    
    