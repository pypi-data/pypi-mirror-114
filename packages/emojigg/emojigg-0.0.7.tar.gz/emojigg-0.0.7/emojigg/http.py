import aiohttp

from typing import (
    Optional, 
    List, 
    Dict,
    ClassVar
)


from .emoji import Emoji
from .pack import Pack
from .errors import NotImplemented


class Route:
    BASE: ClassVar[str] = 'https://emoji.gg/api'
    
    def __init__(
        self, 
        ext: str = '', 
        **kwargs
    ) -> None:
        self.ext = ext
        self.kwargs = kwargs
    
    @property
    def url(self) -> str:
        return self.BASE + self.ext


class HTTP:
    def __init__(
        self, 
        session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.session = session or aiohttp.ClientSession()
        
    async def request(
        self, 
        method: str, 
        route: Route
    ) -> Dict:
        async with self.session.request(method, route.url, **route.kwargs) as resp:
            if resp.status != 200:
                raise NotImplemented(
                    'This error has not been implemented yet. ' \
                    'We actually dont know the response of this... please give it to the lib deb', 
                    await resp.read()  # I don't know if this is json, we'll return the read version instead.
                )
            return await resp.json() 
    
    async def fetch_emojis(self) -> List[Emoji]:
        """
        |coro|
        
        Retreives approx 5000 emojis from the website.
        
        Returns
        -------
        List[Emoji]
        """
        return await self.request('GET', Route('/'))
    
    async def fetch_packs(self) -> List[Pack]:
        """
        |coro|
        
        Retreives packs from the website.
        
        Returns
        -------
        List[Pack]
        """
        return await self.request('GET', Route('/packs'))
    
    async def fetch_statistics(self) -> Dict:
        """
        |coro|
        
        Retreives statistics about this website.
        
        Returns
        -------
        Dict
        """
        return await self.request('GET', Route(params={
            'request': 'stats'
        }))
        
    async def fetch_categories(self) -> Dict:
        """
        |coro|
        
        Retreives categories from the website. Fetches the current categories
        
        Returns
        -------
        Dict
        """
        return await self.request('GET', Route(params={
            'request': 'categories'
        }))