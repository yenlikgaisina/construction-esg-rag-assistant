import os

from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate

from basic_chain import get_model
from filter import ensemble_retriever_from_docs
from local_loader import load_txt_files
from memory import create_memory_chain
from rag_chain import make_rag_chain


def create_full_chain(retriever, openai_api_key=None, chat_memory=ChatMessageHistory()):
    model = get_model("ChatGPT", openai_api_key=openai_api_key)
    system_prompt = """
You are a specialist AI research assistant for ESG, sustainability, climate risk,
circular economy, embodied carbon, and overheating in the built environment.

Use only the context provided below and the user's chat history.

Your job is to help built-environment professionals, students, policymakers,
and sustainability teams understand complex research in clear language.

Rules:
1. If the answer is not in the provided context, say: "I don't have enough evidence in the uploaded sources to answer that confidently."
2. Do not invent facts, regulations, numbers, or citations.
3. Explain technical concepts in plain English.
4. When useful, structure the answer into:
   - Quick answer
   - Why it matters
   - Practical actions
   - Source notes
5. If the question is broad, give a clear summary and suggest better follow-up questions.

Context:
{context}

Question:
"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )

    rag_chain = make_rag_chain(model, retriever, rag_prompt=prompt)
    chain = create_memory_chain(model, rag_chain, chat_memory)
    return chain


def ask_question(chain, query):
    response = chain.invoke(
        {"question": query},
        config={"configurable": {"session_id": "foo"}}
    )
    return response


def main():
    load_dotenv()

    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()

    docs = load_txt_files()
    ensemble_retriever = ensemble_retriever_from_docs(docs)
    chain = create_full_chain(ensemble_retriever)

    queries = [
        "What are the most important ESG topics in construction?",
        "Explain embodied carbon in simple terms.",
        "How can UK homes reduce overheating risk?",
    ]

    for query in queries:
        response = ask_question(chain, query)
        console.print(Markdown(response.content))


if __name__ == '__main__':
    # this is to quiet parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()
