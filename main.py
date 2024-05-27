import aiohttp
import aiofiles
import asyncio
from bs4 import BeautifulSoup

# Список URL
urls = [
    "https://regex101.com/",
    "https://docs.python.org/3/this-url-will-404.html",
    "https://www.nytimes.com/guides/",
    "https://www.mediamatters.org/",
    "https://1.1.1.1/",
    "https://www.politico.com/tipsheets/morning-money",
    "https://www.bloomberg.com/markets/economics",
    "https://www.ietf.org/rfc/rfc2616.txt"
]

# Функция для получения HTML страницы
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Failed to fetch {url}: Status {response.status}")
                return ""
    except Exception as e:
        print(f"Exception while fetching {url}: {str(e)}")
        return ""

# Функция для парсинга и записи ссылок
async def parse_and_write_links(session, url, file):
    html = await fetch(session, url)
    if not html:
        return

    soup = BeautifulSoup(html, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    async with aiofiles.open(file, 'a') as f:
        for link in links:
            await f.write(link + '\n')

# Основная функция
async def main(urls, output_file):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_write_links(session, url, output_file) for url in urls]
        await asyncio.gather(*tasks)

# Запуск
output_file = 'links.txt'
asyncio.run(main(urls, output_file))

