class Planner:
    def build_plan(self, task: str) -> list[str]:
        normalized = task.strip() or "general request"
        return [
            f"Understand task: {normalized}",
            "Select suitable tools or provider",
            "Execute minimal safe workflow",
            "Return a concise result",
        ]
