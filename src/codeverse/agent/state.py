from dataclasses import dataclass, field


@dataclass
class ProposedChange:
    path: str
    summary: str
    diff: str
    new_content: str


@dataclass
class AgentResult:
    output: str
    steps: list[str] = field(default_factory=list)
    proposed_changes: list[ProposedChange] = field(default_factory=list)
    approval_required: bool = False
