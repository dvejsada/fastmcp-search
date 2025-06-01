from fastmcp import FastMCP
from pydantic import Field
from typing import Annotated
from search.main import WebSearch

mcp = FastMCP("MCP Web search")

websearcher = WebSearch()

@mcp.tool(
    name="search_web",           # Custom tool name for the LLM
    description="Performs a web search.", # Custom description
    tags={"search"}, # Optional tags for organization/filtering
    annotations={"title": "Web search"}
)
async def web_search(
        query: Annotated[str, Field(description="Query to be searched")],
        lang: Annotated[str, Field(description="Search language(eg. en, cs etc.)")],
        ) -> str:
    """Performs a web search."""

    global websearcher

    print(f"Performing web search for query: {query}")

    response: str = await websearcher.perform_simple_search(query, lang)

    print(f"Returning answer for query: {query}")

    return response

@mcp.tool(
    name="extract_webpage",           # Custom tool name for the LLM
    description="Extracts webpage for given URL.", # Custom description
    tags={"search"}, # Optional tags for organization/filtering
    annotations={"title": "Extract URL"}
)
async def url_extraction(
        url: Annotated[str, Field(description="URL to be extracted.")],
        query: Annotated[str, Field(description="User's query that prompted extraction.")],
        ) -> str:
    """Extracts relevant content from URL."""

    global websearcher

    print(f"Extracting URL: {url}")

    response: str = await websearcher.extract_url(url, query)

    print(f"Extracted URL: {url}")

    return response


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=4200,
        log_level="info",
        path="/mcp"
    )