from pydantic import BaseModel


class MessageEntities(BaseModel):
    """Message entities."""

    names: list[str] = []
    phone_numbers: list[str] = []
    email_addresses: list[str] = []
    physical_addresses: list[str] = []
