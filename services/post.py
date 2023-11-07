from db import Session
from db.models.posts import Post


async def create_post(theme_text: str, text: str, theme_id: int = None):
    db = Session()
    obj = {
        'theme_text': theme_text,
        'text': text,
    }
    if theme_id:
        obj['theme_id'] = theme_id
    post_obj = Post(**obj)
    db.add(post_obj)
    await db.flush()
    await db.commit()
    return post_obj
