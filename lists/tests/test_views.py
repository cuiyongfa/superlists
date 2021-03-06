from django.test import TestCase
from lists.models import Item, List
from lists.forms import ItemForm
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
# Create your tests here.


class HomePageTest(TestCase):

    # maxDiff = None
    # def test_home_page_returns_correct_html(self):
    #     request = HttpRequest()
    #
    #     response = home_page(request)
    #     expected_html = render_to_string('home.html')
    #     self.assertMultiLineEqual(response.content.decode(), expected_html)
    #
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_rends_home_template(self):
        reponse = self.client.get('/')
        self.assertIsInstance(reponse.context['form'], ItemForm)

    # def test_only_saves_when_necessary(self):
    #     self.client.get('/')
    #     self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_display_only_items_for_that_list(self):
        list_1 = List.objects.create()
        Item.objects.create(text='item 1', list=list_1)
        Item.objects.create(text='item 2', list=list_1)
        list_2 = List.objects.create()
        Item.objects.create(text='item 1 of 2', list=list_2)
        Item.objects.create(text='item 2 of 2', list=list_2)
        response = self.client.get('/lists/%d/' % (list_1.id, ))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 1 of 2')
        self.assertNotContains(response, 'item 2 of 2')

    def test_list_use_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'view_list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()

        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

class NewListTest(TestCase):
    def test_can_save_a_POST_request_1(self):
        self.client.post('/lists/new', data={'text': '新待办事项'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '新待办事项')

    def test_redircts_after_POST(self):
        response = self.client.post('/lists/new', data={'text':  '新待办事项'})
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the_only_one_list_urll')
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id, ))

    def test_validation_errors_can_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expect_error = '输入不能为空'
        self.assertContains(response, expect_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_new_item_can_save_a_POST_request_to_an_exiting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/lists/%d/' % (correct_list.id,), data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post('/lists/%d/' % (correct_list.id,),
                                    data={'text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()

        response = self.client.post(
        '/lists/%d/' % (list_.id,),
        data={'text': ''}
         )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_list.html')
        expected_error = "输入不能为空"
        self.assertContains(response, expected_error)





