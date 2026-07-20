import pytest

pytest.importorskip("langchain_core")

from src.agents.orchestrator import _build_classifier_prompt
from src.agents.hr_agent import _build_prompt as _build_hr_prompt
from src.agents.tech_agent import _build_prompt as _build_tech_prompt
from src.agents.finance_agent import _build_prompt as _build_finance_prompt


def test_new_agent_modules_expose_prompt_builders():
    classifier_prompt = _build_classifier_prompt()
    hr_prompt = _build_hr_prompt()
    tech_prompt = _build_tech_prompt("it")
    finance_prompt = _build_finance_prompt()

    assert "hr" in classifier_prompt.messages[0].prompt.template
    assert "IT Support" in tech_prompt.messages[0].prompt.template
    assert "Finance" in finance_prompt.messages[0].prompt.template
    assert "Human Resources" in hr_prompt.messages[0].prompt.template
