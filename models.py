from pydantic import BaseModel
from typing import List, Dict, Any

class ImportantFile(BaseModel):
    path: str
    description: str

class AnalyzeResponse(BaseModel):
    summary: str
    technologies: List[str]
    important_files: List[ImportantFile]
    architecture: str
    notes: List[str] 