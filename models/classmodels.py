from pydantic import BaseModel

class Response(BaseModel):
    """Class to define the response schema."""
    response:str