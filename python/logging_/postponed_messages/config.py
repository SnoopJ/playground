import json
import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AcmeConfig:
    log_dir: Path = Path("/tmp/anvil-service.log")
    log_level: str = "INFO"
    anvil_weight: int = 999
