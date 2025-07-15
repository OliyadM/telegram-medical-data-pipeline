# schemas.py
from pydantic import BaseModel

class TopProduct(BaseModel):
    product_name: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int
    messages_with_images: int
    messages_with_text_only: int

class MessageSearchResult(BaseModel):
    message_id: int
    message_text: str
    message_date: str
    channel_name: str
