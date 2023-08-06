from pydantic import BaseModel


class BotUser(BaseModel):
    user_id: str
    name: str


class Chat(BaseModel):
    chat_id: int
    sender_id: str
    sender: str
    str_message: str
