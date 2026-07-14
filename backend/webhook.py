import httpx

async def dispatch_webhook(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10)
            response.raise_for_status()
        except httpx.HTTPError as e:
            log_error(e)

'''
If you’re working at scale or with untrusted endpoints, you should also:

Set a retry policy
Add rate-limiting
Support webhook signature verification (HMAC)
'''