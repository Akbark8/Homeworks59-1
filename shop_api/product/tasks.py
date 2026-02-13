from decimal import Decimal

from celery import shared_task
from django.db.models import F

from .models import Product


@shared_task
def increase_product_price(product_id: int, percent: int = 10) -> str:
    """Увеличивает цену товара на указанный процент."""
    multiplier = Decimal(1) + (Decimal(percent) / Decimal(100))
    updated = Product.objects.filter(id=product_id).update(price=F('price') * multiplier)

    if not updated:
        return f'Товар с id={product_id} не найден.'

    return f'Цена товара с id={product_id} увеличена на {percent}%.'


def queue_price_increase(product_id: int, percent: int = 10):
    """Пример запуска задачи через .delay()."""
    return increase_product_price.delay(product_id=product_id, percent=percent)