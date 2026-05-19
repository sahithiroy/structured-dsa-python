from pydantic import BaseModel
from typing import List, Optional


class DataTrendsAndForecast(BaseModel):
    overall_trend: Optional[str]
    latest_trend: Optional[str]
    forecast: Optional[List[float]]