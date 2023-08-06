import aiohttp

from typing import (
    Optional, 
    List, 
    Union,
    Dict,
    Any
)

from .http import HTTP
from .pack import Pack
from .emoji import Emoji


class Client:
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        session = session or aiohttp.ClientSession()
        self._http = HTTP(session)
        
    async def fetch_emojis(self) -> List[Emoji]:
        """
        |coro|
        
        Retreives approx 5000 emojis from the website.
        
        Returns
        -------
        List[Emoji]
        """
        data = await self._http.fetch_emojis()
        return [Emoji(entry) for entry in data]
    
    async def fetch_packs(self) -> List[Pack]:
        """
        |coro|
        
        Retreives packs from the website.
        
        Returns
        -------
        List[Pack]
        """
        data = await self._http.fetch_packs()
        return [Pack(entry) for entry in data]
    
    async def fetch_statistics(self) -> Dict:
        """
        |coro|
        
        Retreives statistics about this website.
        
        Returns
        -------
        Dict
        """
        return await self._http.fetch_statistics()
    
    async def fetch_categories(self) -> Dict:
        """
        |coro|
        
        Retreives categories from the website. Fetches the current categories
        
        Returns
        -------
        Dict
        """
        return await self._http.fetch_categories()
    
    def find(
        self,
        iterable: List[Any],
        check: Any
    ) -> Union[None, Any]:
        """
        Find something within a list according to your check.
        
        Parameters
        ----------
        iterable: List[Any]
            The thing you want to iterate through
        check: Any
            The check func you want to use.
            
        Examples
        -------
        Using Lambda:
        ```python
        data = await client.fetch_emojis()
        specific_emoji = client.find(data, check=lambda emoji: emoji.name == 'this')
        ```
        
        Using a check func:
        ```python
        data = await client.fetch_emojis()
        
        def check(emoji):
            return emoji.name == 'this'
            
        specific_emoji = client.find(data, check=check)
        ```
        """
        for iter in iterable:
            if check(iter):
                return iter
        return None


    