from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import time


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
    # 伊迪丝访问首页，不小心提交了一个空待办事项
# 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys(' ')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)


# 首页刷新了，显示一个错误消息
# 提示待办事项不能为空
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, '输入不能为空')
# 她输入一些文字，然后再次提交，这次没问题了
        inputbox = self.get_item_input_box()
        inputbox.send_keys('     买牛奶')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. 买牛奶')
# 她有点儿调皮，又提交了一个空待办事项

        inputbox = self.get_item_input_box()
        inputbox.send_keys(' ')
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

# 在清单页面她看到了一个类似的错误消息
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, '输入不能为空')
        # 输入文字之后就没问题了

        self.get_item_input_box().send_keys('       Make tea'+Keys.ENTER)
        self.wait_for_row_in_list_table('1. 买牛奶')
        self.wait_for_row_in_list_table('2. Make tea')
        # time.sleep(10)





