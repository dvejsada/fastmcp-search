"""
Component for text summarization using LLMs
"""
from .connectors.bedrock_api import BedrockConnector
import os
import json

class Summarizer:

    def __init__(self):
        self.bedrock_client = BedrockConnector()
        self.summarizer_model_id = os.getenv("SUMMARIZER_MODEL_ID", "anthropic.claude-3-5-haiku-20241022-v1:0")

    async def summarize_text(self, text_to_summarize: str, query: str) -> str:
        """
        Summarizes provided text using LLMs
        :param text_to_summarize: Text to be summarized
        :param query: Query to base the summarization on
        :return: String with summarized text
        """
        prompt = ("You are a content extraction assistant. Your task is to analyze webpage content and return only the portions that are directly relevant to a given query. "
                  "INSTRUCTIONS:1. You will receive extracted webpage content and a specific query, "
                  "2. Identify all sections, paragraphs, or passages that contain information relevant to the query,"
                  "3. Return the relevant content EXACTLY as it appears in the original text - do not summarize, paraphrase, or modify the wording in any way)"
                  "4. Include complete sentences and paragraphs to maintain context"
                  "5. If multiple sections are relevant, return all of them"
                  "6. If very little content is relevant, return only the small relevant portion"
                  "7. If substantial content is relevant, return the larger relevant portions"
                  "8. Do not add your own commentary, explanations, or any introductory text")

        prompt += f"Query: {query}, Content: {text_to_summarize}."

        try:
            # Call summarizing model
            summarized_text: str = await self.bedrock_client.invoke_model(prompt, self.summarizer_model_id)

            return summarized_text

        except Exception as e:
            print(f"Error during summarizing: {e}")
            # Fall back to original results
            return text_to_summarize
