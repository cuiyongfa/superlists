from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import unittest


class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #首页
        self.browser.get('http://localhost:8000')
        #标题和头部都包含“待办事项”
        self.assertIn('待办事项', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项', header_text)

        #要求输入“待办事项”

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '输入待办事项')
        #输入了“买鱼饵”
        inputbox.send_keys('买鱼饵')
        #回车，页面更新
        #待办事项表格显示 “1.买鱼饵”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        table = self.browser.find_element_by_id('id_list_table')
        rows =table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1.买鱼饵' for row in rows), "新待办事项不显示")

        self.fail('finish the test')


if __name__ == '__main__':
    unittest.main(warnings='ignore')

