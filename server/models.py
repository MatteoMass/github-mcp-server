from pydantic import BaseModel
from typing import List

class IssuesList(BaseModel):
    issues: List[str]