"""
Simple Python API wrapper for https://scrapper.scurra.space/

"""
from urllib.parse import quote
import json
import requests
import aiohttp


def get_page(
    url: str,
    api_key: str,
    attempts: int = 3,
    proxy_country: int = 0,
    user_agent: str = "",
    use_selenium: bool = False,
    referer: str = "",
    base_api_url: str = "https://scrapper.scurra.space/api/get?url=",
) -> dict:
    """Simple sync wrapper function for scrapper API"""
    api_url = "{}{}".format(base_api_url, quote(url))
    if user_agent and user_agent != "":
        api_url += "&ua={}".format(quote(user_agent))
    if proxy_country > 0:
        api_url += "&country={}".format(proxy_country)
    if use_selenium:
        api_url += "&use_selenium=1"
    if referer:
        api_url += "&referer={}".format(referer)
    api_url += "&attempts={}".format(attempts)
    retries = 0
    good = False

    while retries < attempts and not good:
        retries += 1
        data = requests.get(
            api_url,
            headers={
                "Authorization": "api-key {}".format(api_key),
            },
        )
        try:
            result = json.loads(data.text)
        except:
            result = {
                "html": "",
                "error": True,
                "error_text": "Json response from API is invalid",
            }
        else:
            good = True
    return result


async def get_page_async(
    url: str,
    api_key: str,
    attempts: int = 3,
    proxy_country: int = 0,
    user_agent: str = "",
    referer: str = "",
    use_selenium: bool = False,
    base_api_url: str = "https://scrapper.scurra.space/api/get?url=",
) -> dict:
    """Simple async wrapper function for scrapper API"""
    api_url = "{}{}".format(base_api_url, quote(url))
    if user_agent and user_agent != "":
        api_url += "&ua={}".format(quote(user_agent))
    if proxy_country > 0:
        api_url += "&country={}".format(proxy_country)
    if use_selenium:
        api_url += "&use_selenium=1"
    if referer:
        api_url += "&referer={}".format(referer)
    api_url += "&attempts={}".format(attempts)

    retries = 0
    good = False
    result = {"html": "", "error": True}
    while retries < attempts and not good:
        retries += 1
        headers = {
            "Authorization": "api-key {}".format(api_key),
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                api_url,
                headers=headers,
            ) as response:
                try:
                    result = json.loads(await response.text())
                except TypeError:
                    result = {
                        "html": "",
                        "error": True,
                        "error_text": "Json response from API is invalid",
                    }
                else:
                    good = True
    return result
