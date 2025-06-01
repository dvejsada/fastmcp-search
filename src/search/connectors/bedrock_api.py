import boto3
import json
import os
from botocore.client import BaseClient


class BedrockConnector:
    """
    Connector for AWS Bedrock AI services, providing simplified interfaces
    for text generation, reranking, and other Bedrock model interactions.
    """

    def __init__(self):
        """
        Initialize the BedrockConnector.
        """
        # Initialize client with explicit credentials if provided

        self.region_name = os.getenv("AWS_REGION")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if self.aws_access_key_id and self.aws_secret_access_key and self.region_name:
            self.client: BaseClient = boto3.client(
                service_name="bedrock-runtime",
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )
        else:
            raise ValueError("Missing AWS credentials")


    async def invoke_model(self,
                      prompt: str,
                      model_id: str,
                      max_tokens: int = 8000,
                      temperature: float = 0.5) -> str:
        """
        Generate text using an Anthropic model.

        Args:
            prompt: The prompt for text generation
            model_id: Model ID to be used
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)

        Returns:
            Generated text response
        """

        # Request for anthropic models
        if "anthropic" in model_id:

            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "temperature": temperature,
                    "max_tokens": 8000,
                    "messages": [
                      {
                        "role": "user",
                        "content": [
                          {
                            "type": "text",
                            "text": prompt
                          }
                        ]
                      }
                    ]
                })
            )

            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]

        # Request for amazon models
        elif "amazon" in model_id:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "inferenceConfig": {
                        "maxTokens": 5120,
                        "temperature": 0.7
                    },
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                })
            )

            response_body = json.loads(response["body"].read())
            return response_body["output"]["message"]["content"][0]["text"]



        else:
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                })
            )

            response_body = json.loads(response["body"].read())
            return response_body["content"][0]["text"]

    async def rerank(self, model_id: str, query:str, documents: list) -> dict:
        """
        Reranks provides list based on a query
        :param model_id: Model to be used for reranking
        :param query: Query for reranking
        :param documents: List of documents to rerank
        :return: Reranked list of documents
        """
        response = self.client.invoke_model(
            modelId=model_id,
            body=json.dumps({
                "query": query,
                "documents": documents,
                "top_n": len(documents),
                "api_version": 2
            })
        )

        response_body = json.loads(response["body"].read())

        return response_body
