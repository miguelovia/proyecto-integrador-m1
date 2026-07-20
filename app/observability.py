from contextlib import contextmanager
from typing import Any, Dict, Iterator, Optional

from langfuse import Langfuse, propagate_attributes
from langfuse._client.span import LangfuseSpan
from langfuse.langchain import CallbackHandler

from app.config import settings

_langfuse_client: Optional[Langfuse] = None


def get_langfuse_client() -> Langfuse:
    """Singleton Langfuse client, built from the credentials in .env."""
    global _langfuse_client
    if _langfuse_client is None:
        _langfuse_client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
    return _langfuse_client


@contextmanager
def start_trace(
    name: str,
    input_data: Dict[str, Any],
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Iterator[LangfuseSpan]:
    """Open one Langfuse trace for a full support ticket.
    """
    client = get_langfuse_client()
    with client.start_as_current_observation(name=name, input=input_data) as span:
        with propagate_attributes(
            session_id=session_id,
            user_id=user_id,
            tags=["support-router"],
        ):
            yield span


def get_langchain_handler() -> CallbackHandler:
    """A LangChain callback handler
    """
    return CallbackHandler()


def get_trace_url(trace_id: str) -> Optional[str]:
    return get_langfuse_client().get_trace_url(trace_id=trace_id)
