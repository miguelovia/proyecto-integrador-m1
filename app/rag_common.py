"""Bloques compartidos para los agentes RAG de cada departamento.

Cada módulo de agente bajo src/agents/ (hr_agent.py, tech_agent.py,
finance_agent.py, legal_agent.py) es un archivo delgado y autocontenido que
solo declara su clave de departamento + una frase de dominio, y llama a este
módulo para construir su retriever + prompt grounded + retrieval chain.
Mantener la lógica de construcción en un solo lugar evita que las reglas de
grounding (responder solo con el contexto, citar fuentes, admitir cuando no
se sabe) diverjan entre departamentos.
"""

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.config import settings
from app.vectorstore import get_retriever

# NOTE: {{context}} is deliberately double-braced so that .format() below only
# substitutes department/brief and leaves a single {context} placeholder for
# create_stuff_documents_chain to fill in per-request.
_SYSTEM_TEMPLATE = """You are the {department} specialist assistant for a SaaS company's internal support desk.
Domain: {brief}

Answer the employee's question using ONLY the context below, which comes from official internal documentation.
- If the context does not contain enough information to answer confidently, say so plainly and suggest the \
employee open a ticket with the {department} team instead of guessing.
- Never invent policies, numbers, deadlines, or exceptions that are not stated in the context.
- Keep the answer focused and actionable for an employee — not a general explanation of the topic.
- Finish with a line starting with "Sources:" listing the document names you relied on.

Context:
{{context}}
"""


def build_department_prompt(department: str, brief: str) -> ChatPromptTemplate:
    system = _SYSTEM_TEMPLATE.format(department=department.upper(), brief=brief)
    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{input}"),
        ]
    )


def build_department_chain(department: str, brief: str):
    """Construye una retrieval chain nueva (retriever + prompt grounded + LLM)
    para un departamento.
    """
    llm = ChatOpenAI(
        model=settings.rag_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
    retriever = get_retriever(department)
    prompt = build_department_prompt(department, brief)
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, combine_docs_chain)
