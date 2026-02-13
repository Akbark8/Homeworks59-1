# Примеры задач Celery

## 1) Задача через `.delay()`
Увеличение цены товара на процент в фоне.

```python
from product.tasks import queue_price_increase

# увеличит цену товара id=5 на 15%
queue_price_increase(product_id=5, percent=15)
```

Задача: `product.tasks.increase_product_price`.

## 2) Задача по расписанию через `crontab`
Каждую ночь в `03:00` удаляются просроченные коды подтверждения старше 24 часов.

Настройка в `CELERY_BEAT_SCHEDULE`:
- task: `accounts.tasks.clear_expired_confirmation_codes`
- schedule: `crontab(hour=3, minute=0)`

## 3) Задача через SMTP
Отправка приветственного письма после регистрации:

```python
from accounts.tasks import send_welcome_email

send_welcome_email.delay(email='user@example.com', username='user123')
```

Требуются SMTP-переменные окружения:
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_USE_TLS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`