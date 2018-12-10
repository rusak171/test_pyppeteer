import asyncio
import pyppeteer
from pyppeteer import launch


URL = 'https://www.olx.ua/obyavlenie/prodam-bmw-x-5-IDBVXf6.html#582b4ef667'
PROXY = 'http://185.110.211.174:59123'
pyppeteer.DEBUG = True


def save_content(content, filename='olx.html'):
    with open(filename, mode='w') as h:
        h.write(content)
    print('Page saved.')


async def main():
    print('Started process...')
    browser = await launch(args=['--no-sandbox', '--proxy-server={}'.format(PROXY)], headless=False)
    # browser = await launch(args=['--no-sandbox', '--proxy-server={}'.format(PROXY)])
    # context = await browser.createIncognitoBrowserContext()
    # page = await context.newPage()
    page = await browser.newPage()
    print('Setting page parameters...')
    await page.setViewport({'width': 1366, 'height': 768})
    await page.setJavaScriptEnabled(True)
    print('Go to url:', URL)
    await page.goto(URL)
    await page.screenshot({'path': 'screen1.png'})
    await asyncio.sleep(5)
    # content = await page.content()
    # save_content(content)

    # Try to click on element to open phone number
    selector = 'div[class*="atClickTracking"]'
    # selector = 'li > a[href*="contact"]'
    # elem = await page.querySelector(selector)
    # print('Element:', elem)
    print('Wait for element...')
    elem = await page.waitForSelector(selector=selector)
    print('Selected element:', elem)
    print('Clicking...')

    #  Click on selector
    # clickOptions = {'delay': 350}
    # await asyncio.wait([
    #     page.waitForNavigation(),
    #     page.click(selector, clickOptions),
    # ])
    # await page.click(selector, clickOptions)
    # await page.waitForNavigation()
    # print('Clicked!')

    #  Another click method
    js_code = '''() => {
        var selector = '%s';
        function main(selector) {
        var elem = document.querySelector(selector);
                var res = 0;
                if (elem != null) {
                    elem.click();
                    res = 100;
                } else {
                    res = -101;
                }
                return res;
        }
        return main(selector);
    }''' % selector
    # print('js_code:', js_code)
    res = await page.evaluate(js_code)
    if int(res) > 0:
        print('Clicked.')
    await asyncio.sleep(3)

    # Check result
    print('Checking result...')
    res_selector = 'strong.xx-large'
    element = await page.querySelector(res_selector)
    phone = await page.evaluate('(element) => element.textContent', element)
    print('Scraped phone:', phone.strip())

    content = await page.content()
    save_content(content)
    # await page.waitForSelector(selector='div[class*="overh"] > span[style*="none"]', hidden=True)
    await page.screenshot({'path': 'screen2.png'})
    await page.close()
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
