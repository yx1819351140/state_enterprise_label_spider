from playwright.sync_api import sync_playwright
from lxml import etree
from state_enterprise_label_spider.utils import Tool_Library
import time


def run(playwright):
    browser = playwright.firefox.launch(headless=False, slow_mo=100, args=['--no-sandbox'], ignore_default_args=['--enable-automation', '--mute-audio',])
    # browser = playwright.firefox.launch(headless=False,
    #                                     # proxy={"server": "per-context"},
    #                                     slow_mo=100,
    #                                      # args=['--no-sandbox',],
    #                                      # ignore_default_args=['--enable-automation', '--mute-audio',],
    #                                      # proxy={'server': '223.109.206.202:9641'}, )

    #  '--blink-settings=imagesEnabled=false',  chromium 禁止加载图片
    # route 的参数默认是通配符，也可以传递编译好的正则表达式对象
    context = browser.new_context(viewport={'width': 1400, 'height': 900}, )
    # context = browser.new_context(viewport={'width': 1400, 'height': 900}, proxy={"server": "175.22.188.2:4224"})
    # context.route(re.compile(r"(\.png$)|(\.jpg$)|(\.jpeg$)|(\.css$)|(\.js$)|(\.gif$)"), lambda route: route.abort())
    # context.route(re.compile(r"(\.png$)|(\.jpg$)|(\.jpeg$)"), lambda route: route.abort())
    # context.route(re.compile(r"(\.png$)|(\.jpeg$)"), lambda route: route.abort())
    # 监控 请求和响应 Subscribe to "request" and "response" events.

    page = context.new_page()
    # page.on("request", lambda request: print(">>", request.method, request.url))
    # page.on("response", lambda response: print("<<", response.status, response.url))
    # page.on("response", lambda response: deal_data(response.text()) if 'getZoneParkCompanyDetail' in response.url else ...)
    page.goto('https://www.nmpa.gov.cn/datasearch/home-index.html#category=yp')
    time.sleep(3)

    page.click('xpath=//a[contains(text(), "关闭")]')
    page.fill('xpath=//input[@data-intro="输入需要查询的关键词"]', '国')
    # page.click('xpath=//div[@class="el-input-group__append"]')
    # time.sleep(3)

    with page.expect_popup() as popup_info:
        page.click('xpath=//div[@class="el-input-group__append"]')
    new_page = popup_info.value

    new_page.click('xpath=//a[contains(text(), "关闭")]')
    new_page.click('xpath=//div[@class="el-input el-input--mini el-input--suffix"]/input[@placeholder="请选择"]')
    new_page.click('xpath=//li/span[contains(text(), "20条/页")]')
    new_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    i = 1
    end_page = 7977
    while i <= end_page:
        try:
            new_page.fill('xpath=//input[@type="number"]', str(i))
            new_page.click('xpath=//input[@type="number"]')
            new_page.keyboard.press("Enter")
            time.sleep(0.1)
            print(i+1, new_page.title())
            root = etree.HTML(new_page.content())
            tr_list = root.xpath('//div[@class="el-table__body-wrapper is-scrolling-none"]//tr')
            for tr in tr_list:
                dict = {}
                dict['approval_number'] = tr.xpath('./td[2]//p/text()')[0] if tr.xpath('./td[2]//p/text()') else ''
                dict['product_name'] = tr.xpath('./td[3]//p/text()')[0] if tr.xpath('./td[3]//p/text()') else ''
                if dict['product_name'] == '':
                    dict['product_name'] = ''.join(tr.xpath('./td[3]//text()')).strip() if tr.xpath('./td[3]//text()') else ''
                dict['company_name'] = tr.xpath('./td[4]//p/text()')[0] if tr.xpath('./td[4]//p/text()') else ''
                if dict['company_name'] == '':
                    dict['company_name'] = ''.join(tr.xpath('./td[4]//text()')).strip() if tr.xpath('./td[4]//text()') else ''
                dict['drug_code'] = tr.xpath('./td[4]//p/text()')[0] if tr.xpath('./td[4]//p/text()') else ''
                sql = Tool_Library.generate_sql('nmpa_drugCompany', dict)
                Tool_Library.execute_sql(tidb=True, database='acq_com_gs', sql=sql)
                Tool_Library.push_kafka('collect_nmpa_drugCompany', dict)
                print(dict)

            # new_page.click('xpath=//button[@class="btn-next"]')
            i += 1
        except Exception as e:
            # print(e)
            continue


with sync_playwright() as playwright:
    run(playwright)
