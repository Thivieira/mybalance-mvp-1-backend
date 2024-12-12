from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Defines the structure of the error message.
    """
    mesage: str
