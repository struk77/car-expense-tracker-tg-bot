import httpx
from datetime import date

from config import BASE_CURRENCY

_cache: dict[str, float] = {}
_cache_date: date | None = None


def parse_amount(text: str) -> tuple[float, str] | None:
    text = text.strip().replace(",", ".")
    try:
        amount = float(text)
        return (amount, BASE_CURRENCY) if amount > 0 else None
    except ValueError:
        pass
    parts = text.split()
    if len(parts) == 2:
        try:
            amount = float(parts[0])
            return (amount, parts[1].upper()) if amount > 0 else None
        except ValueError:
            pass
    return None


async def to_base(amount: float, currency: str) -> float:
    if currency == BASE_CURRENCY:
        return amount
    rate = await _get_rate(currency)
    return round(amount * rate, 2)


async def is_valid(code: str) -> bool:
    if code == BASE_CURRENCY:
        return True
    try:
        await _get_rate(code)
        return True
    except Exception:
        return False


async def _get_rate(currency: str) -> float:
    global _cache, _cache_date
    today = date.today()
    if _cache_date != today:
        _cache = {}
        _cache_date = today

    if currency not in _cache:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.frankfurter.app/latest",
                params={"from": currency, "to": BASE_CURRENCY},
            )
            resp.raise_for_status()
            data = resp.json()
            _cache[currency] = data["rates"][BASE_CURRENCY]

    return _cache[currency]
