from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

db_dir = "chroma_db"
embedding = get_embedding_function()
db = Chroma(persist_directory=db_dir, embedding_function=embedding)

# Prompt fixo
PROMPT = """ Você é um assistente treinado para responder com base no conteúdo abaixo. Se não encontrar a resposta exata, seja honesto e diga que a informação não está disponível no documento.

{context}
---

Pergunta: {question}
"""

model = Ollama(model="mistral", temperature=0.9)

def rerank_results(results):
    return sorted(results, key=lambda x: x[1])


def query(query_text: str):
    results = db.similarity_search_with_score(query_text, k=10)
    reranked = rerank_results(results)[:5]
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in reranked])


    prompt_template = ChatPromptTemplate.from_template(PROMPT)
    formatted_prompt = prompt_template.format(context=context_text, question=query_text)

    response_text = model.invoke(formatted_prompt)
    sources = [doc.metadata.get("id", "Desconhecida") for doc, _ in results]

    return {"answer": response_text, "sources": sources}
