from pydantic import BaseModel
from typing import List


# 🔹 State (observation)
class State(BaseModel):
    state: List[float]


# 🔹 Action input
class Action(BaseModel):
    action: int


# 🔹 Reset request
class ResetRequest(BaseModel):
    task: str = "medium"


# 🔹 Step response
class StepResponse(BaseModel):
    state: List[float]
    reward: float
    done: bool
