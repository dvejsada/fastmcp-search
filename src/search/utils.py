
def normalize_response(list_of_results) -> str:
    """
    Transforms the list of results into string.

    :param list_of_results: List of results to be transformed
    :return: String with results as text
    """
    text_response = "Search results:\n----\n"

    for result in list_of_results:
        text_response += (f"Url: {result["url"]}\n"
                          f"Relevance: {result["score"]}\n"
                          f"Title: {result["title"]}\n"
                          f"Content: {result["content"]}\n"
                          f"----\n"
                          )

    return text_response