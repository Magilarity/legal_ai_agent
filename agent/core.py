from openai import OpenAI
from db.schema import Session, Document
import pinecone


class LegalAgent:
    def __init__(self, api_key: str, db_url: str, pinecone_key: str):
        self.client = OpenAI(api_key=api_key)
        pinecone.init(api_key=pinecone_key, environment="us-west1-gcp")
        self.index = pinecone.Index("legal-docs")

    def retrieve(self, query: str, top_k: int = 5):
        # embedding query
        emb = self.client.embeddings.create(input=query)["data"][0]["embedding"]
        res = self.index.query(emb, top_k=top_k)
        docs = []
        with Session() as session:
            for match in res.matches:
                doc = session.query(Document).get(match.id)
                docs.append(doc)
        return docs

    def answer(self, query: str):
        ctx = "\n---\n".join([d.content for d in self.retrieve(query)])
        prompt = f"Context:\n{ctx}\nQuestion: {query}\nAnswer:"
        return self.client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )
