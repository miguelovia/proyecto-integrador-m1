# Decisiones técnicas

Resumen de las tecnologías usadas en el proyecto y por qué se eligieron.

## Orquestación

El orquestador (`src/agents/orchestrator.py`) clasifica cada ticket con una sola llamada estructurada
a un LLM y, con base en esa clasificación, enruta condicionalmente al RAG agent del departamento
correspondiente — no es un agente autónomo con tool-calling. El problema de negocio es "muchos
tickets se enrutan mal", lo que exige que la decisión de ruteo sea **explícita, barata y con
`reasoning` visible**, en vez de una decisión implícita difícil de auditar.

## Estructura de agentes

Cada departamento vive en su propio módulo bajo `src/agents/` (`hr_agent.py`, `tech_agent.py`,
`finance_agent.py`, `legal_agent.py`), cada uno con su propia colección de documentos en Chroma y su
propio prompt grounded, en vez de un único retriever genérico compartido filtrado por metadata. Esto
evita que un filtro mal aplicado mezcle contexto de un departamento con el de otro.

## Modelo de LLM

Se usa OpenAI (`gpt-4o`) para el clasificador, los RAG agents y el evaluador, ya que es el proveedor
con el que ya se cuenta y el más ampliamente adoptado, con buen soporte de function calling /
structured output.

## Vectorización

Se usa Chroma como vector store, con una colección independiente por departamento. Los embeddings son
locales (`sentence-transformers`), no de OpenAI: evita costo por token y llamadas de red al reindexar,
y no depende de que `OPENAI_API_KEY` esté configurada para correr los tests de retrieval.

## Observability

Se usa **Langfuse** para mantener la traza de cada ejecución (clasificación → retrieval → generación →
evaluación) y poder inspeccionar el detalle de cualquier ticket, incluyendo los mal enrutados o con
respuestas de baja calidad.
