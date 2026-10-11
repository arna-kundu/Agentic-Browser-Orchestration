from pydantic import BaseModel
class BrowserPlan(BaseModel):
    action:str
    task:str