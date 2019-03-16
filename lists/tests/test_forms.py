from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ERROR_MESSAGE


class ItemFormTest(TestCase):

    def test_form_render_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="输入待办事项"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ERROR_MESSAGE])

