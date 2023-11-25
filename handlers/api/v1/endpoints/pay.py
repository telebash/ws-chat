import base64
from datetime import datetime

import requests
from loguru import logger
from fastapi import APIRouter, Depends

from db import Session
from core.config import settings
from schemas.pay import PaySchema
from services.user import user_paid
from services.subscription import create_payment

router = APIRouter()


@router.post('/')
async def subscribe(data: PaySchema = Depends(PaySchema.as_form)):
    user_id = int(data.AccountId)
    if data.Status == 'Completed':
        await create_payment(
            user_id=user_id,
            currency=data.Currency,
            total_amount=int(data.Amount),
        )
        await user_paid(user_id)
        logger.info(f'User {user_id} paid')
        return {'code': 0}
    if data.Status == 'Authorized':
        cp = f"{settings.CP_PUBLIC_ID}:{settings.CP_SECRET_KEY}".encode("utf-8")
        headers = {
            'Authorization': f'Basic {base64.b64encode(cp).decode("utf-8")}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        payload = {
            'TransactionId': data.TransactionId,
        }
        response = requests.get(
            "https://api.cloudpayments.ru/payments/get",
            headers=headers,
            json=payload,
        )
        if not response.ok:
            return {'code': 1}
        await create_payment(
            user_id=user_id,
            currency=data.Currency,
            total_amount=int(data.Amount),
        )
        await user_paid(user_id)
        logger.info(f'User {user_id} paid')
        return {'code': 0}
