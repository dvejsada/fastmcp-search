"""
Component for web search.
"""
from .summarize import Summarizer
from .extract import Extractor
from .search import Searcher
from .rerank import Reranker
from .utils import normalize_response


class WebSearch:

    def __init__(self):
        """
        Initialize the class.
        """

        self.summarizer = Summarizer()
        self.searcher = Searcher()
        self.extractor = Extractor()
        self.reranker = Reranker()

    async def perform_simple_search(self, query: str, lang: str) -> str:
        """
        Searches for provided query and returns answer along with citations.

        :param query: Query to search
        :param lang: Language to search in
        :return: Response to query along with sources
        """

        search_response: list = await self.searcher.search_web(query, lang)

        text_response = normalize_response(search_response)

        return text_response

    async def extract_url(self, url: str, query: str) -> str:
        """
        Extracts content from URL and summarizes the relevant content.
        :param url: URL to be extracted
        :param query: Query for summarization
        :return: Summarized content
        """

        extracted_url: dict = await self.extractor.extract_from_webpage(url)

        if extracted_url["success"]:
            summarized_text = await self.summarizer.summarize_text(extracted_url["content"], query)
            extracted_url['content'] = summarized_text

            return extracted_url['content']

        else:
            return "No data can be extracted from provided URL."

    async def perform_deep_research(self, topic: str, lang: str) -> str:
        """
        Performs deep research on the given topic.

        :param topic: Topic to search
        :param lang: Language for the search and outcome

        :return: Text of the research with links and references.
        """

        deep_research_response = ""

        return deep_research_response
