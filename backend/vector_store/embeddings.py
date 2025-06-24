from openai import OpenAI
import os
import json

OpenAI.api_key = os.getenv("OPENAI_API_KEY")


class Embeddings:
    def __init__(self):
        self.client = OpenAI()

    def create_embedding(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )
        return response.data[0].embedding
