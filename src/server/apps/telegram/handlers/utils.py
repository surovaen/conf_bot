from pathlib import Path
from typing import Optional, Tuple, Union

import aiohttp
from django.conf import settings

from server.apps.payments.enums import ProductTypes
from server.apps.telegram.database.managers import (
    payment_db_manager,
    promo_db_manager,
    user_db_manager,
)


async def check_promo(promo: str) -> Tuple[bool, Optional[int]]:
    """"""
    promo = await promo_db_manager.get(promo=promo)
    if not promo:
        return False, None

    return True, promo.discount


async def get_payment_url(payment_data: dict) -> str:
    """Генерация ссылки на оплату."""
    product = payment_data.get('product')
    price = payment_data.get('price')
    payment_id = payment_data.get('payment_id')
    phone_number = payment_data.get('user').phone_number

    data = {
        'do': 'link',
        'products': [
            {
                'name': product.label,
                'price': str(price),
                'quantity': '1'
            }
        ],
        'sys': '',
        'order_id': str(payment_id),
        'customer_phone': phone_number,
    }

    data.pop('products')
    data.update(
        {
            'products[0][name]': product.label,
            'products[0][price]': str(price),
            'products[0][quantity]': '1'
        }
    )
    query_params = '&'.join('='.join(item) for item in data.items())
    payment_url = '{url}?{query_params}'.format(
        url=settings.PRODAMUS_URL,
        query_params=query_params,
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(payment_url) as response:
            payment_url = await response.text()

    return payment_url


async def create_payment(
        user_id: Union[int, str],
        product: ProductTypes,
        event_uuid: str,
        price: Union[int, str],
        ticket: str = None,
) -> str:
    """Функция создания платежа и генерации ссылки на оплату."""
    user = await user_db_manager.get(user_id)
    payment_data = {
        'user': user,
        'product': product,
        'product_id': event_uuid,
        'price': price,
    }
    if ticket is not None:
        payment_data['ticket'] = ticket
    payment_id = await payment_db_manager.create(payment_data)
    if ticket is not None:
        payment_data.pop('ticket')
    payment_data.update(
        {
            'payment_id': payment_id,
        }
    )

    return await get_payment_url(payment_data)


def get_media_path(file: str) -> Path:
    """Функция формирования полного пути до файла."""
    return Path(settings.MEDIA_ROOT).joinpath(file)
