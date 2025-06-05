from pydantic import BaseModel
from typing import List

class IssuesList(BaseModel):
    issues: List[str]

class PullRequestList(BaseModel):
    pull_requests: List[str]

class BranchList(BaseModel):
    branches: List[str]

class CommitsList(BaseModel):
    commits: List[str]

class RepoStats(BaseModel):
    stars: int
    forks: int
    watchers: int
    open_issues: int