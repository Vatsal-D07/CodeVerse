from codeverse.config.settings import get_settings


class SafetyGuard:
    def can_run_shell(self) -> bool:
        return get_settings().safety.allow_shell
