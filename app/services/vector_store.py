from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

class CustomEmbeddings(Embeddings):
    def embed_documents(self, texts):
        from .embeddings import get_embeddings
        return get_embeddings(texts)

    def embed_query(self, text):
        from .embeddings import get_embeddings
        return get_embeddings([text])[0]

def create_vector_store(chunks):
    return FAISS.from_texts(chunks, CustomEmbeddings())
