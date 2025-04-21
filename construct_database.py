from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma
import pdfplumber
from pathlib import Path

pdf_dir = "pdfs"
db_dir = "chroma_db"


def load_documents():
    documents = []
    for pdf_path in Path(pdf_dir).glob("*.pdf"):
        extracted_docs = extract_with_pdfplumber(str(pdf_path))
        documents.extend(extracted_docs)
    return documents


def extract_with_pdfplumber(pdf_path):
    docs = []
    filename = Path(pdf_path).name 

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            tables = page.extract_tables()
            content = text or ""

            for table in tables:
                table_data = []
                headers = table[0] 
                for row in table[1:]:
                    row_data = {headers[j]: row[j] for j in range(len(headers))}
                    table_data.append(row_data)

                content += (
                    "\n\n[TABELA: Conteúdo extraído da página — possivelmente grade curricular ou dados estruturados]\n"
                    + str(table_data)
                )

            docs.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": filename,
                        "page": i + 1
                    }
                )
            )
    return docs


def split_documents(documents: list[Document]):
    splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=40,
        tokens_per_chunk=256,
        model_name="intfloat/e5-base-v2",
    )
    return splitter.split_documents(documents)


def add_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=db_dir, embedding_function=get_embedding_function())
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Foram adicionados: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    # .pdf:6:2"
    # Page Source : Page Number : Chunk Index
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks


def generate_db():
    documents = load_documents()
    chunks = split_documents(documents)
    add_chroma(chunks)


generate_db()
