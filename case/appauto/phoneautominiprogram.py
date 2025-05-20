import time
from selenium.webdriver.common.by import By
from autowebview import AutoWebView
from loguru import logger

"""
webview自动化 执行层
"""

class AutoMiniProgram(AutoWebView):

    def __init__(self, phone, text=None):
        super(AutoMiniProgram, self).__init__(phone)
        #super(AutoMiniProgram, self).senftext(text)


    def openSearch(self):
        logger.info("点击搜索按钮")
        # logger.info(self.driver.page_source)
        search_btn = self.driver.find_element(
            By.XPATH,
            '//wx-view[contains(@class, "search-index--app-style-index-search-btn-semicircle") or contains(text(), "搜索")]'
        )
        logger.info(f"search_btn outerHTML: {search_btn.get_attribute('outerHTML')}")
        logger.info(f"search_btn text: {search_btn.text}")
        logger.info(f"search_btn page_source: {self.driver.title}")
        search_btn.click()
        logger.info("已点击搜索按钮")

    def miniprogram(self, text):
        logger.info("mini")


if __name__ == '__main__':

    from phoneobject import PO
    phone =PO.getPhoneSerial()
    AutoMiniProgram(phone,'魔卡图鉴').openSearch()

