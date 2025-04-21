from langchain_community.embeddings import HuggingFaceBgeEmbeddings

model_name = "intfloat/e5-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embedding_model = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)


def get_embedding_function():
    return embedding_model
