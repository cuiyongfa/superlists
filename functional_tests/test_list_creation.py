from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        #首页
        self.browser.get(self.server_url)
        #标题和头部都包含“待办事项”
        self.assertIn('待办事项', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项', header_text)


        #要求输入“待办事项”

        inputbox = self.get_item_input_box()
        self.assertEqual(inputbox.get_attribute('placeholder'), '输入待办事项')
        #输入了“买鱼饵”
        inputbox.send_keys('买鱼饵')
        #回车，页面更新ma
        #待办事项表格显示 “1.买鱼饵”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        one_list_url = self.browser.current_url
        self.assertRegex(one_list_url, '/lists/.+')

        self.wait_for_row_in_list_table('1.买鱼饵')

        #输入页面重新显示
        #输入'买鱼竿‘
        inputbox =self.get_item_input_box()
        inputbox.send_keys('买鱼竿')
        inputbox.send_keys(Keys.ENTER)

        #页面再次更新，显示两个事项
        self.wait_for_row_in_list_table('1.买鱼饵')
        self.wait_for_row_in_list_table('2.买鱼竿')

        #另一人访问网站
        #新首页启动新会话
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #新主页没有另一人的内容

        self.browser.get(self.server_url)
        time.sleep(1)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买鱼饵', page_text)
        self.assertNotIn('买鱼竿', page_text)

        #第二人输入清单
        #得到他的URL
        #显示他的内容不显示另一人的内容
        inputbox = self.get_item_input_box()
        inputbox.send_keys('买牛奶')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        two_list_url = self.browser.current_url
        # time.sleep(1)
        self.assertRegex(two_list_url, '/lists/.+')
        self.assertNotEqual(two_list_url, one_list_url)
        self.wait_for_row_in_list_table('1.买牛奶')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买鱼饵', page_text)

        self.fail('完成测试')



