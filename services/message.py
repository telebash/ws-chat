from typing import List

from sqlalchemy import select

from db import Session
from schemas.message import SaveMessage, SaveMessageBase, SaveMessages
from services import ChatEnum
from db.models.message import Message


async def get_messages(
        project_id: int,
        chat: ChatEnum,
        skip: int = 0,
        limit: int = 100
) -> List[Message]:
    db = Session()
    query = select(Message).where(
        Message.project_id == project_id,
        Message.chat == chat
    ).order_by(Message.datetime.desc()).offset(skip).limit(limit)
    messages = await db.execute(query)
    messages = messages.scalars().all()
    await db.close()
    return messages


async def save_messages(data: SaveMessages) -> None:
    db = Session()
    models = []
    for message in data.messages:
        model = Message(
            type=message.type,
            chat=data.chat,
            sender=message.sender,
            data=message.data,
            datetime=message.datetime,
            project_id=data.project_id,
            post_id=message.post_id,
            image_id=message.image_id,
        )
        models.append(model)
    db.add_all(models)
    await db.flush()
    await db.commit()


async def save_message(data: SaveMessage) -> None:
    db = Session()
    model = Message(
        type=data.type,
        chat=data.chat,
        sender=data.sender,
        data=data.data,
        datetime=data.datetime,
        project_id=data.project_id
    )
    db.add(model)
    await db.flush()
    await db.commit()
