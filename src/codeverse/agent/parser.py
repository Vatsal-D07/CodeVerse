class IntentParser:
    def parse(self, prompt: str) -> dict[str, str]:
        action = "chat"
        normalized = prompt.lower()
        if any(keyword in normalized for keyword in {"edit", "modify", "update", "change", "fix", "refactor", "rewrite", "rename"}):
            action = "edit"
        elif "analyze" in normalized:
            action = "analyze"
        return {"action": action, "prompt": prompt}
