from pydantic import BaseModel
from entities.playlist import ChatHistory


class NewMessage(BaseModel):
    content: str

    def to_chat_history(self, is_bot: bool):
        return ChatHistory.model_validate({ **self.model_dump(), 'bot': is_bot })
