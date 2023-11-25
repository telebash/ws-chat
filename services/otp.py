import random

from sqlalchemy import select

from db import Session
from db.models.otp import Otp, OtpTypeEnum


async def get_otp_by_code(code: str):
    db = Session()
    query = select(Otp).where(Otp.code == code)
    otp = await db.execute(query)
    otp = otp.scalars().first()
    await db.close()
    return otp


async def get_otp_by_user_id(user_id: int):
    db = Session()
    query = select(Otp).where(Otp.user_id == user_id)
    otp = await db.execute(query)
    otp = otp.scalars().first()
    await db.close()
    return otp


async def create_otp(user_id: int, otp_code: str, otp_type: OtpTypeEnum):
    db = Session()
    otp = Otp(
        code=otp_code,
        type=otp_type,
        user_id=user_id,
    )
    db.add(otp)
    await db.flush()
    await db.commit()
    await db.close()
    return otp


async def delete_otp(id: int):
    db = Session()
    otp = await db.get(Otp, id)
    if not otp:
        return False
    await db.delete(otp)
    await db.commit()
    await db.close()
    return True


async def generate_and_create_otp(user_id: int, otp_type: OtpTypeEnum):
    otp_code = ''.join(random.choices('0123456789', k=6))
    otp = await get_otp_by_code(otp_code)
    if otp:
        return await generate_and_create_otp(user_id, otp_type)
    otp = await create_otp(user_id, otp_code, otp_type)
    return otp
