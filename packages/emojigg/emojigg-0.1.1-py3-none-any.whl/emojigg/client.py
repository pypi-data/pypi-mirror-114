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
        return [Emoji(self._http, entry) for entry in data]
    
    async def fetch_packs(self) -> List[Pack]:
        """
        |coro|
        
        Retreives packs from the website.
        
        Returns
        -------
        List[Pack]
        """
        data = await self._http.fetch_packs()
        return [Pack(self._http, entry) for entry in data]
    
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

    