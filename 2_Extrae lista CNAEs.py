import asyncio
from playwright.async_api import Playwright, async_playwright
from bs4 import BeautifulSoup

async def extract_and_save_cnaes(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://app.bde.es/rss_www/Ratios")

    try:
        await page.wait_for_selector("#sector", timeout=5000)
        sector_html = await page.inner_html("#sector")

        soup = BeautifulSoup(sector_html, "html.parser")

        cnaes = []
        for option in soup.find_all("option"):
            value = option["value"]
            text = option.text
            cnaes.append(f"{value} - {text}")  # Formato "valor - texto"

        # Guardar los CNAEs en un archivo
        with open("downloads/lista CNAEs.txt", "w", encoding="utf-8") as f:  # encoding para caracteres especiales
            for cnae in cnaes:
                f.write(cnae + "\n")

        print("Archivo 'lista CNAEs.txt' creado con éxito.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await extract_and_save_cnaes(playwright)

asyncio.run(main())