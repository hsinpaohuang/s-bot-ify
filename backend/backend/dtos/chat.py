from pydantic import BaseModel
from entities.playlist import ChatHistory


class NewMessage(BaseModel):
    content: str

    def to_chat_history(self, is_bot: bool):
        return ChatHistory.model_validate({ **self.model_dump(), 'bot': is_bot })

class ChatMessage(BaseModel):
    id: str
    content: str
    timestamp: float
    bot: bool

    @classmethod
    def from_chat_history(cls, chat_history: ChatHistory):
        return cls.model_validate({
            **chat_history.model_dump(),
            'timestamp': chat_history.timestamp.timestamp(),
        })
