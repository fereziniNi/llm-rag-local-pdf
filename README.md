# 🤖 Local PDF Chatbot with LLM (LangChain + Ollama + Mistral)

A local intelligent assistant that answers questions about PDF files using **LangChain**, **Ollama (Mistral)**, **ChromaDB**, and embeddings from `intfloat/e5-base-v2`. Works completely offline — ideal for analyzing documents like curricula, reports, or technical papers.

> 📂 Ask questions from one or more local PDFs — with text, table extraction, and smart semantic chunking!

---

## 📸 Demo

![demo](example-demo.png) <!-- Add a gif or screenshot here if available -->

---

## 🚀 Tech Stack

- Python 3.11+
- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.com/) (model: `mistral`)
- Embeddings from [`intfloat/e5-base-v2`](https://huggingface.co/intfloat/e5-base-v2)
- [ChromaDB](https://www.trychroma.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber) for text and table extraction

---

## 🧠 How It Works

1. Extracts text and tables from all PDFs in the folder.
2. Splits text into semantic chunks using Sentence Transformers.
3. Generates embeddings and stores them locally in ChromaDB.
4. Performs semantic search with reranking.
5. Uses **Mistral** via Ollama to generate context-based answers.

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-user/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure you have `ollama` installed and the `mistral` model downloaded:

```bash
ollama pull mistral
```

---

## 📂 Project Structure

- `pdfs/` → Place your PDF files here
- `chroma_db/` → Local vector store
- `query.py` → RAG query logic with reranking and prompting
- `get_embedding_function.py` → Embedding wrapper

---

## ▶️ Usage

### 1. Generate the vector DB from PDFs

```bash
python main.py
```

### 2. Start the local chatbot

```bash
python chat.py
```

Now ask anything about the documents!  
Example:

```
You: What is the total workload of the Artificial Intelligence course?
```

---

## 🧪 Example Response

```
🤖 Chatbot: The total workload for "Artificial Intelligence" is 60 hours.
📚 Sources: curriculum.pdf:3:2
```

---

## 📌 Notes

- Works **100% offline** — no internet needed.
- Supports multiple PDFs.
- Smart extraction of **structured tables**.
- Ideal for educational, legal, academic, or technical use.

---

## 🧑‍💻 Author

Developed by [Your Name](https://www.linkedin.com/in/your-linkedin/)  
Contributions, ideas, and feedback are welcome!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).