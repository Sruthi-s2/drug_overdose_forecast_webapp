from pydantic import BaseModel, Field
from typing import Dict

class OverdoseDeaths(BaseModel):
    year: int
    month: str
    indicator: str
    no_of_deaths: float
    state: Dict[str, str] = Field(..., example={"code": "OH", "name": "Ohio"})
