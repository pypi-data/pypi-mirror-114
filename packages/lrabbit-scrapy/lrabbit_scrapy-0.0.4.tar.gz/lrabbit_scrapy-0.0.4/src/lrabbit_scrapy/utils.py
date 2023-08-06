import aiohttp
from parsel import Selector





async def get_html_by_url(url, headers=None, proxy=None):
    res = await get_res_by_url(url, headers, proxy)
    text = await res.text()
    return text


async def get_css_selector_by_url(url, headers=None, proxy=None):
    kwargs = {'url': url}
    if headers:
        kwargs['headers'] = headers
    if proxy:
        kwargs['proxy'] = proxy
    html = await get_html_by_url(url, headers=headers, proxy=proxy)
    selector = Selector(html)
    return selector


async def get_res_by_url(url, headers=None, proxy=None):
    async with aiohttp.ClientSession() as session:
        kwargs = {'url': url}
        if headers:
            kwargs['headers'] = headers
        if proxy:
            kwargs['proxy'] = proxy
        res = await session.get(**kwargs)
        return res


async def download_by_url(url, file_path, headers=None, proxy=None):
    res = await get_res_by_url(url, headers, proxy)
    with open(file_path, 'wb') as f:
        while True:
            chunk = await res.content.read(1024)
            if chunk:
                f.write(chunk)
            else:
                break
    return file_path
