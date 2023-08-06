# aioSENZ package 
[![PyPI](https://img.shields.io/pypi/v/aiosenz)](https://pypi.org/project/aiosenz) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aiosenz) [![PyPI - License](https://img.shields.io/pypi/l/aiosenz?color=blue)](https://github.com/milanmeu/aiosenz/blob/main/COPYING)

An async Python wrapper for the nVent Raychem SENZ RestAPI.

## Installation
```bash
pip install aiosenz
```

## OAuth2
This package offers an `AbstractSENZAuth`, where you should handle the OAuth2 tokens and provide a valid access token in `get_access_token()`. You can use `SENZAuth` if you don't want to handle the OAuth2 tokens yourself.

## Grant type

`SENZAuth` uses the Authorization Code grant type. This requires a Client ID and Client Secret, more information is available in [the RestAPI documentation](https://api.senzthermostat.nvent.com).

## Scopes
AioSENZ uses the `restapi` and `offline_access` scope, this is set as default in SENZAuth and should be set in the OAuth2 client if you are using the AbstractSENZAuth class. The OpenID (`openid`) and OpenID Profile (`profile`) scopes are not supported, because nVent recommends to use the RestAPI Account instead.

## Example
```python
from asyncio import run
from aiosenz import SENZAuth, SENZAPI
import httpx

async def main():
    async with httpx.AsyncClient() as httpx_client:
        senz_auth = SENZAuth(
            httpx_client,
            "YOUR_CLIENT_ID",
            "YOUR_CLIENT_SECRET",
            redirect_uri="http://localhost:8080/auth/callback",
        )
        uri, state = await senz_auth.get_authorization_url()
        print("Authorization URI: ", uri)
        authorization_response = input("The authorization response URL: ")
        await senz_auth.set_token_from_authorization_response(authorization_response)
        
        senz_api = SENZAPI(senz_auth)
        thermostats = await senz_api.get_thermostats()
        for thermostat in thermostats:
            print(f"{thermostat.name} temperature: {thermostat.current_temperatue}")
        await senz_auth.close()

run(main())
```
