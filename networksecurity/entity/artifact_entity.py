from dataclasses import dataclass
from typing import List

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str