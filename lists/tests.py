from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        reponse = self.client.post('/', data={'item_text': '新待办事项'})
        self.assertIn('新待办事项', reponse.content.decode())
        self.assertTemplateUsed(reponse, 'home.html')





