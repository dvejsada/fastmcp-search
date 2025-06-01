from tavily import AsyncTavilyClient, InvalidAPIKeyError, MissingAPIKeyError, UsageLimitExceededError
import os

class Tavily:
    def __init__(self):

        self.client = AsyncTavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    async def tavily_search(self, query, result_number: int) -> list|str:
        """Performing a search query"""
        try:
            context = await self.client.search(query=query, include_answer=False, max_results=result_number)
        except InvalidAPIKeyError:
            return "No responses can be found due to invalid API key"
        except MissingAPIKeyError:
            return "No responses can be found due to missing API key"
        except UsageLimitExceededError:
            return "Usage limit exceeded. Please check your plan's usage limits or consider upgrading."

        return context['results']

    async def extract_url(self, url: str) -> dict:

        urls = [url]

        response: dict = await self.client.extract(urls=urls, extract_depth="advanced", include_images=False)

        if len(response["results"]) == 1:
            return {"success": True, "content": response["results"][0]["raw_content"]}

        else:
            return {"success": False, "content": None}


    async def tavily_extract(self, urls: list) -> str:
        """Extracts the contents of the webpage."""

        response = await self.client.extract(urls=urls, extract_depth="advanced",include_images=False)

        extracted_data: str = ""

        # Printing the extracted raw content
        for result in response["results"]:
            extracted_data += f"URL: {result['url']}"
            extracted_data += f"Raw Content: {result['raw_content']}\n"

        if response["failed_results"]:
            extracted_data += f"Following URLs cannot be extracted:"
            for failed_result in response["failed_results"]:
                extracted_data += f"URL: {failed_result['url']}."
                extracted_data += f"Error: {failed_result['error']}."

        return extracted_data

