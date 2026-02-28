"""AI service — Google Gemini 2.5 Flash integration with deterministic stub fallback."""

import logging
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _stub_suggest_description(title: str) -> str:
    """Deterministic stub — returns a predictable description for testing/CI."""
    return (
        f"This task involves working on '{title}'. "
        f"Key deliverables include: planning, implementation, testing, and documentation. "
        f"Estimated complexity: medium. Priority: normal."
    )


def _stub_daily_plan(tasks: list) -> str:
    """Deterministic stub — returns a predictable daily plan for testing/CI."""
    if not tasks:
        return "No tasks assigned. Consider picking up new work from the backlog."

    plan_items = []
    for i, task in enumerate(tasks, 1):
        title = task.get("title", "Untitled")
        status = task.get("status", "unknown")
        plan_items.append(f"{i}. [{status.upper()}] {title}")

    return (
        "Here's your daily plan:\n"
        + "\n".join(plan_items)
        + "\n\nFocus on in-progress items first, then move to reviews."
    )


async def suggest_description(title: str) -> dict:
    """Generate a task description from a short title.

    Uses Gemini 2.5 Flash when available, falls back to deterministic stub.
    """
    if settings.AI_STUB_MODE:
        return {
            "suggestion": _stub_suggest_description(title),
            "is_stub": True,
        }

    # Live Gemini call
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = (
            "You are a project management assistant. Given a short task title, "
            "generate a clear, concise task description (2-3 sentences) that includes "
            "the goal, key deliverables, and suggested approach.\n\n"
            f"Task title: {title}"
        )

        response = model.generate_content(prompt)
        suggestion = response.text.strip()
        return {"suggestion": suggestion, "is_stub": False}

    except Exception as e:
        logger.error(f"Gemini call failed: {e}", exc_info=True)
        # Graceful degradation — fall back to stub
        return {
            "suggestion": _stub_suggest_description(title),
            "is_stub": True,
            "warning": f"LLM unavailable, using fallback. Error: {str(e)}",
        }


async def suggest_daily_plan(user_tasks: list) -> dict:
    """Generate a concise daily plan based on the user's current tasks.

    Uses Gemini 2.5 Flash when available, falls back to deterministic stub.
    """
    task_dicts = [{"title": t.title, "status": t.status.value} for t in user_tasks]

    if settings.AI_STUB_MODE:
        return {
            "suggestion": _stub_daily_plan(task_dicts),
            "is_stub": True,
        }

    # Live Gemini call
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")

        tasks_summary = "\n".join(
            f"- {t['title']} (status: {t['status']})" for t in task_dicts
        )

        prompt = (
            "You are a project management assistant. Given a list of tasks with their "
            "statuses, create a concise daily plan (5-7 bullet points) prioritizing "
            "in-progress work, then reviews, then new items.\n\n"
            f"Tasks:\n{tasks_summary}"
        )

        response = model.generate_content(prompt)
        suggestion = response.text.strip()
        return {"suggestion": suggestion, "is_stub": False}

    except Exception as e:
        logger.error(f"Gemini call failed: {e}", exc_info=True)
        return {
            "suggestion": _stub_daily_plan(task_dicts),
            "is_stub": True,
            "warning": f"LLM unavailable, using fallback. Error: {str(e)}",
        }
