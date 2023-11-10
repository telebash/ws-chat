from datetime import datetime
from dateutil.relativedelta import relativedelta
from db.engine import Session

from db.models.user import User


async def subscription_checker(user: User):
    if user.is_admin_user:
        return user
    if not user.paid:
        return user
    current_date = datetime.now()
    subscription_date = user.subscription_date
    payment = user.payments[0]
    if payment.total_amount == 200000:
        subscription_duration = relativedelta(days=1)
    elif payment.total_amount == 1000000:
        subscription_duration = relativedelta(days=7)
    elif payment.total_amount == 2000000:
        subscription_duration = relativedelta(months=1)
    subscription_expiry_date = subscription_date + subscription_duration

    if current_date > subscription_expiry_date:
        await user.update(session=Session(), paid=False)

    return user


async def user_created_at_checker(user: User):
    if user.is_admin_user:
        return user
    current_date = datetime.now()
    created_at = user.created_at
    creat_duration = relativedelta(days=7)
    creat_expiry_date = created_at + creat_duration

    if current_date > creat_expiry_date:
        await user.update(session=Session(), free_use_bool=False)
        return None

    return user
