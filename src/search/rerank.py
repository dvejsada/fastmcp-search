from .connectors.bedrock_api import BedrockConnector

import json
import os

class Reranker:

    def __init__(self):
        self.bedrock_client = BedrockConnector()
        self.rerank_model_id = os.getenv("RERANK_MODEL_ID", "cohere.rerank-v3-5:0")

    async def rerank(self, query: str, results: list) -> list:
        """
        Rerank search results by relevance to the query.

        Args:
            query: The search query or research question
            results: List of search results to rerank

        Returns:
            Reranked and filtered list of results
        """
        if not results:
            return []

        # Prepare documents for reranking
        documents = []
        for result in results:
            # Create a document with title and content
            doc = f"Title: {result['title']}\nContent: {result['content']}"
            documents.append(doc)

        try:
            # Call rerank model
            response_body: dict = await self.bedrock_client.rerank(self.rerank_model_id, query, documents)


            # Add relevance scores to the original results
            reranked_results = []
            for item in response_body.get("results", []):
                idx = item["index"]
                score = item["relevance_score"]

                result = results[idx].copy()
                result["relevance_score"] = float(score)
                reranked_results.append(result)

            # Sort by relevance score (highest first)
            reranked_results.sort(key=lambda x: x["relevance_score"], reverse=True)

            return reranked_results

        except Exception as e:
            print(f"Error during reranking: {e}")
            # Fall back to original results with default relevance scores
            for result in results:
                result["relevance_score"] = result.get("relevance_score", 1.0)
            return sorted(results, key=lambda x: x.get("relevance_score", 0), reverse=True)