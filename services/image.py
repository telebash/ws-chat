from db import Session
from db.models.image import Image


async def create_image(url: str, style: str, seed: int, prompt: str):
    db = Session()
    obj = {
        'url': url,
        'style': style,
        'seed': seed,
        'prompt': prompt
    }
    image_obj = Image(**obj)
    db.add(image_obj)
    await db.flush()
    await db.commit()
    return image_obj
