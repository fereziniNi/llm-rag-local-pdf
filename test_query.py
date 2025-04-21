from query import query
from langchain_community.llms.ollama import Ollama

PROMPT_FORMAT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""
def test_sigla_materias():
    assert query_and_validate(
        question="Qual é a titulação, Regime de trabalho e Área da professora Aline Raquel?",
        expected_response="Mestra, RDE, Letras",
    )

def test_objetivos():
    assert query_and_validate(
        question="Qual é o objetivo da matéria Auditoria e Segurança de Sistemas?",
        expected_response="Identificar e avaliar a integridade e segurança de dados. Avaliar riscos na segurança de sistemas de informação."
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query(question)
    prompt = PROMPT_FORMAT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="mistral")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Resultado de avaliação inválido. Não é possível determinar se é 'verdadeiro' ou 'falso'."
        )