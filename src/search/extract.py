"""
Component for extracting text from webpage
"""
from .connectors.tavily_api import Tavily


class Extractor:

    def __init__(self):
        """
        Initialize the Extractor class
        """
        self.tavily = Tavily()

    async def extract_from_webpage(self, url: str) -> dict:

        response: dict = await self.tavily.extract_url(url)

        return response