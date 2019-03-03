from django.test import TestCase
from lists.models import Item, List
# Create your tests here.


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


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


class NewListTest(TestCase):
    def test_can_save_a_POST_request_1(self):
        self.client.post('/lists/new', data={'item_text': '新待办事项'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '新待办事项')

    def test_redircts_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':  '新待办事项'})
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the_only_one_list_urll')
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id, ))

class NewItemTest(TestCase):

    def test_new_item_can_save_a_POST_request_to_an_exiting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/lists/%d/add_item' % (correct_list.id,), data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()

        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % (correct_list.id,),
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))



class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_=List()
        list_.save()

        first_item = Item()
        first_item.list = list_
        first_item.text = '第一个条目'
        first_item.save()

        second_item = Item()
        second_item.text = '第二个条目'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item =saved_items[1]

        self.assertEqual(first_saved_item.text, '第一个条目')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '第二个条目')
        self.assertEqual(second_saved_item.list, list_)









