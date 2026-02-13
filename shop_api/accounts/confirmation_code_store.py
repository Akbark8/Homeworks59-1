from django.conf import settings


CONFIRMATION_CODE_TTL_SECONDS = 5 * 60


def _get_redis_client():
    from redis import Redis

    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


def _build_key(user_id: int) -> str:
    return f'confirmation_code:{user_id}'


def save_confirmation_code(user_id: int, code: str) -> None:
    redis_client = _get_redis_client()
    redis_client.setex(_build_key(user_id), CONFIRMATION_CODE_TTL_SECONDS, code)


def consume_confirmation_code(user_id: int, code: str) -> bool:
    redis_client = _get_redis_client()
    key = _build_key(user_id)

    stored_code = redis_client.get(key)
    if stored_code != code:
        return False

    redis_client.delete(key)
    return True