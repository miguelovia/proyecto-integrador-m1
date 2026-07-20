import pytest

pytest.importorskip("langchain_core")

from src.agents import finance_agent, hr_agent, legal_agent, tech_agent  # noqa: E402
from src.agents.orchestrator import DEPARTMENT_BRIEFS, _build_classifier_prompt  # noqa: E402

_AGENT_MODULES = [hr_agent, tech_agent, finance_agent, legal_agent]


def test_classifier_prompt_mentions_all_departments():
    prompt = _build_classifier_prompt()
    system_message = prompt.messages[0].prompt.template
    for department in DEPARTMENT_BRIEFS:
        assert department in system_message


def test_each_agent_module_is_grounded_and_department_specific():
    for module in _AGENT_MODULES:
        department = module.DEPARTMENT
        brief = module.DEPARTMENT_BRIEFS[department]

        prompt = module._build_prompt(department)
        system_message = prompt.messages[0].prompt.template

        assert department.upper() in system_message
        assert brief in system_message
        assert "{context}" in system_message
        assert "ONLY the context" in system_message


def test_orchestrator_briefs_match_each_agent_modules_own_brief():
    for module in _AGENT_MODULES:
        department = module.DEPARTMENT
        assert DEPARTMENT_BRIEFS[department] == module.DEPARTMENT_BRIEFS[department]
