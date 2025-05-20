import os
import platform
from loguru import logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from configs import CHROMEDRIVERVERSION
import re


class AutoWebView:

    def __init__(self, phone):
        self.phone = phone
        self.serial = phone.serial
        app = phone.current_app()
        logger.info(f'app: {app}')
        optionsData = {
            'androidPackage': app['package'],
            'androidDeviceSerial': self.serial,
            'androidUseRunningApp': True,
            'androidProcess': "com.tencent.mm:appbrand0",
        }
        logger.info(f'options:{optionsData}')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('androidPackage', optionsData['androidPackage'])
        options.add_experimental_option('androidDeviceSerial', optionsData['androidDeviceSerial'])
        options.add_experimental_option('androidUseRunningApp', optionsData['androidUseRunningApp'])
        options.add_experimental_option('androidProcess', optionsData['androidProcess'])
        
        path = ChromeDriverManager(driver_version=CHROMEDRIVERVERSION).install()
        self.driver = webdriver.Chrome(executable_path=path, options=options)
        self.driver.implicitly_wait(3)


    def getPidName(self):
        pidcommand = f'adb -s {self.serial} shell dumpsys activity top| {"findstr" if platform.system() == "Windows" else "grep"} ACTIVITY'
        logger.info(pidcommand)
        pidcommandtext = os.popen(pidcommand)
        pidText = pidcommandtext.read()
        logger.info(f'pidText: {pidText}')
        app = self.phone.current_app()
        package = app['package']
        pid = None
        for line in pidText.splitlines():
            if package in line:
                match = re.search(r'pid=(\d+)', line)
                if match:
                    pid = match.group(1)
                    break
        if not pid:
            logger.error('未找到对应包名的pid')
            return ''
        logger.info(f'pid: {pid}')

        pidnamecommand = f'adb -s {self.serial} shell ps {pid}'
        logger.info(pidnamecommand)
        pidnamecommandtext = os.popen(pidnamecommand)
        pidNameText = pidnamecommandtext.read()
        logger.info(f'adbshellPidNameText: {pidNameText}')
        pidName = ''
        for line in pidNameText.splitlines():
            if pid in line:
                parts = line.split()
                if len(parts) > 0:
                    pidName = parts[-1]
                    break
        logger.info(f'pidName: {pidName}')
        return pidName if pidName else ''

    def senftext(self, text=None):
        """
        切换到对应url窗口，未指定
        """
        windows = self.driver.window_handles  # 获取所有窗口
        [logger.info(f'当前存在的窗口有：{win}') for win in windows]

        if not text:
            self.driver.switch_to.window(windows[-1])  # 切换最新窗口
            logger.debug(f'window: {windows[-1]}, windowUrl: {self.driver.current_url}')  # 打印窗口和对应url
            logger.debug(f'切换成功')
            return self

        for window in windows:
            self.driver.switch_to.window(window)  # 切换窗口
            logger.debug(f'window: {window}, windowUrl: {self.driver.current_url}')  # 打印窗口和对应url
            if text in self.driver.current_url or text in self.driver.execute_script('return document.documentElement.outerHTML'):
                logger.debug(f'切换成功')
                return self
        else:
            logger.error(f'切换失败，未切换到含有{text}的页面')

    def find_element(self, type_value):
        return self.driver.find_element(type_value['type'], type_value['value'])

    def find_elements(self, type_value):
        return self.driver.find_elements(type_value['type'], type_value['value'])
