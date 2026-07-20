# Support Router — Multi-Agent Ticket Routing (LangChain + Langfuse)

Sistema de routing inteligente para soporte interno de una empresa SaaS. Clasifica automáticamente
las consultas entrantes (HR, IT, Finance, Legal) y las dirige a un agente RAG especializado por
departamento, con trazabilidad completa en Langfuse y un evaluador automático de calidad de
respuesta.

Cada ticket abre **un único trace en Langfuse** que contiene, anidados: la llamada de clasificación,
la recuperación + generación del agente RAG que se eligió, y la llamada del evaluador — todo el
camino de ejecución queda inspeccionable en una sola vista, incluyendo respuestas mal enrutadas o de
baja calidad.

## Estructura del proyecto

```
app/                     # infraestructura compartida (no es "un agente")
  config.py              # settings (modelos, rutas, credenciales) desde .env
  schemas.py             # Pydantic: ClassificationResult, EvaluationScores, RoutingResult
  observability.py       # cliente Langfuse + apertura de traces
  vectorstore.py         # construcción/carga de colecciones Chroma por departamento
  rag_common.py          # builder compartido de prompt+chain grounded (usado por cada agente)
  evaluator.py           # evaluador LLM-judge, escribe scores a Langfuse
src/
  agents/
    orchestrator.py      # clasificador + routing condicional hacia los 4 agentes
    hr_agent.py           # RAG agent de HR
    tech_agent.py         # RAG agent de IT (department key "it")
    finance_agent.py      # RAG agent de Finance
    legal_agent.py         # RAG agent de Legal
  samples.py               # corre tickets de ejemplo end-to-end
  vectorization.py         # indexa/reindexa las colecciones Chroma
  multi_agent_system.py    # CLI interactivo
data/
  hr_docs/                # base de conocimiento (markdown) de HR
  tech_docs/               # base de conocimiento de IT (department key "it")
  finance_docs/            # base de conocimiento de Finance
  legal_docs/              # base de conocimiento de Legal
tests/
decisiones.md              # decisiones técnicas y por qué se tomaron
```

Cada archivo bajo `src/agents/` es un módulo delgado: declara su `DEPARTMENT`, su
`DEPARTMENT_BRIEFS` (una frase de dominio) y expone `get_rag_chain(department)`; toda la lógica de
construcción del retriever + prompt grounded + chain vive una sola vez en `app/rag_common.py` para
que las reglas de "no alucines fuera del contexto" no puedan divergir entre departamentos.

## Setup

1. Crear entorno virtual e instalar dependencias:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configurar variables de entorno:

   ```bash
   cp .env.example .env
   # Editar .env y completar:
   #   OPENAI_API_KEY
   #   LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY (proyecto en https://cloud.langfuse.com,
   #   o tu instancia self-hosted vía LANGFUSE_HOST)
   ```

3. Indexar la base de conocimiento (crea `.chroma/` con una colección por departamento):

   ```bash
   python -m src.vectorization
   ```

4. Correr la demo con tickets de ejemplo:

   ```bash
   python -m src.samples
   ```

   o el chat interactivo:

   ```bash
   python -m src.multi_agent_system
   ```

> Nota: el modelo de embeddings (`sentence-transformers/all-MiniLM-L6-v2`) corre localmente — se
> descarga una sola vez la primera vez que se ejecuta `ingest.py` (requiere internet en ese primer
> arranque) y no consume la API de OpenAI ni cuenta contra tu cuota; solo el LLM (clasificador,
> RAG agents y evaluador) usa `OPENAI_API_KEY`.

## Uso programático

```python
from src.agents.orchestrator import handle_query

result = handle_query("¿Cuántos días de vacaciones tengo al año?", session_id="user-123")

print(result.department)     # "hr"
print(result.confidence)     # 0.0 - 1.0
print(result.answer)         # respuesta grounded en la documentación de HR
print(result.sources)        # ["pto_policy.md"]
print(result.scores)         # EvaluationScores(relevance=5, completeness=5, accuracy=5, ...)
```

## Observability en Langfuse

Cada llamada a `handle_query(...)` abre un trace (`support-ticket`) con:

- **Session/user tracking**: pasa `session_id` / `user_id` para agrupar conversaciones de un mismo
  empleado y filtrar por usuario en el dashboard de Langfuse.
- **Spans anidados**: la clasificación, la recuperación de documentos y la generación del RAG agent,
  y la llamada del evaluador quedan como pasos separados dentro del mismo trace — así se puede ver
  exactamente en qué paso falló un ticket mal enrutado (¿el clasificador eligió mal el departamento?
  ¿el retriever no encontró el documento correcto? ¿el LLM alucinó a pesar de tener el contexto?).
- **Scores continuos**: el evaluador escribe `eval_relevance`, `eval_completeness`, `eval_accuracy` y
  `eval_overall` (0-1) directamente sobre el trace, de forma que se pueden armar alertas o dashboards
  de calidad en Langfuse sin código adicional.

## Agregar un nuevo departamento

1. Crear `data/<nuevo_departamento>_docs/` con uno o más archivos `.md`.
2. Agregar el departamento a `DEPARTMENTS` en `app/config.py` y su carpeta a
   `DATA_DIR_BY_DEPARTMENT` en `app/vectorstore.py` (la clave de departamento y el nombre de la
   carpeta no tienen que coincidir — así "it" vive en `data/tech_docs/`).
3. Crear `src/agents/<nuevo_departamento>_agent.py` siguiendo el patrón de `hr_agent.py` /
   `tech_agent.py` / `finance_agent.py` / `legal_agent.py`: define `DEPARTMENT`, `DEPARTMENT_BRIEFS`
   (una frase describiendo el dominio) y `get_rag_chain(department)` llamando a
   `app/rag_common.py::build_department_chain`.
4. Registrar el nuevo módulo en `src/agents/orchestrator.py`: importar su `DEPARTMENT_BRIEFS` y
   `get_rag_chain`, fusionarlo en `DEPARTMENT_BRIEFS` y agregar su entrada a `_RAG_CHAIN_GETTERS`.
5. Actualizar el `Literal` de `Department` en `app/schemas.py`.
6. Correr `python -m src.vectorization` para indexar los nuevos documentos.

## Tests

```bash
pytest                 # suite rápida (prompts, estructura de datos)
```

## Limitaciones conocidas / próximos pasos

- El evaluador corre siempre después de generar la respuesta (síncrono); en producción conviene
  correrlo async o en batch para no añadir latencia al usuario final.
- No hay retriever híbrido (keyword + semántico) ni re-ranking — para bases de conocimiento grandes
  vale la pena evaluar un re-ranker antes de servir el contexto al RAG agent.
- El clasificador es una única llamada estructurada; no hay una ruta de "no sé a qué departamento
  enrutar esto" que escale a un humano — sería el siguiente paso natural para producción.

Ver `DECISIONES.md` para el razonamiento detrás de cada una de estas decisiones y sus alternativas
consideradas.

## Screenshots
Se adjutan algunas capturas de pantalla de las trazas en langfuse en la carpeta screenshots