from query import query

def chat():
    print("🤖 Chatbot iniciado! Pergunte algo sobre os PDFs ou digite 'sair' para encerrar.\n")
    while True:
        pergunta = input("Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Encerrando o chatbot. Até mais!")
            break

        resposta = query(pergunta)
        print(f"\n🤖 Chatbot: {resposta["answer"]}\n")
        print(f"📚 Fontes: {resposta["sources"]}\n")


chat()