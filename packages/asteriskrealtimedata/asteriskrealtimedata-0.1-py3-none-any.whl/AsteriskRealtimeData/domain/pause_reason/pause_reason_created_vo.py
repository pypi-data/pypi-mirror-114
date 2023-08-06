from dataclasses import dataclass


@dataclass
class PauseReasonCreatedVo:
    pause_code: str
    description: str
