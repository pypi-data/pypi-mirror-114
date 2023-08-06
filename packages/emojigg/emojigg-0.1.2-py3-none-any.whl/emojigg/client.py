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
from . import utils


class Client:
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        session = session or aiohttp.ClientSession()
        self._http = HTTP(session)

    async def fetch_emoji_by(self, type: str, value: Union[str, int]) -> Optional[Emoji]:
        """
        |coro|

        A wrapper for fetching all emojis and using utils to get it.

        Parameters
        ----------
        type: str
            The attr you want to get from the emoji.
        value: Union[str, int]
            The value of the attr you want.
        
        Use Example
        -----------
        ```python
        emoji = await client.fetch_emoji_by('id', 6844)
        ```

        Returns
        -------
        Optional[Emoji]
        """
        emojis = await self.fetch_emojis()
        return utils.find(emojis, check=lambda emoji: getattr(emoji, type) == value)

    async def fetch_pack_by(self, type: str, vaue: Union[str, int]) -> Optional[Pack]:
        """
        |coro|

        A wrapper for fetching all packs and using utils to get it.

        Parameters
        ----------
        type: str
            The attr you want to get from the pack.
        value: Union[str, int]
            The value of the attr you want.
        
        Use Example
        -----------
        ```python
        emoji = await client.fetch_pack_by('id', 6844)
        ```

        Returns
        -------
        Optional[Pack]
        """
        packs = await self.fetch_packs()
        return utils.find(packs, check=lambda emoji: getattr(emoji, type) == value)

    async def fetch_emojis(self) -> List[Emoji]:
        """
        |coro|
        
        Retreives approx 5000 emojis from the website.
        
        Returns
        -------
        List[Emoji]
        """
        return await self._http.fetch_emojis()
    
    async def fetch_packs(self) -> List[Pack]:
        """
        |coro|
        
        Retreives packs from the website.
        
        Returns
        -------
        List[Pack]
        """
        return await self._http.fetch_packs()
    
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

    