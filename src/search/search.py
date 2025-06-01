"""
Component for performing web search
"""
import httpx
import os


class Searcher:

    def __init__(self):

        self.instance_url = os.getenv("SEARXNG_INSTANCE", None)
        if not self.instance_url:
            raise ValueError("No SearxNG instance url provided.")

    async def search_web(self, query: str, lang: str, limit: int = 10) -> list:
        """
        Performs web search for provided query in specified language
        :param query: Query to search
        :param lang: Language to search in
        :param limit: Number of results to be returned
        :return: List of results
        """
        # Set parameters for call
        params: dict = {"q": query, "language": lang, "format": "json"}

        # Make call to SearxNG instance
        async with httpx.AsyncClient() as client:
            response = await client.get(self.instance_url, params=params)
            search_results = response.json()

        results = search_results["results"]

        # If there are more results than the result limit, pass only the most relevant ones
        if len(results) > int(limit):
            results = results[:int(limit)]

        return results




