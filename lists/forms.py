from django import forms
from lists.models import Item

# class ItemForm(forms.Form):
#
#     text = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '输入待办事项1',
#                                                               'class': 'form-control input-lg',
#                                                               }),)

EMPTY_ERROR_MESSAGE = '输入不能为空'


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
        'text': forms.fields.TextInput(attrs={
            'placeholder': '输入待办事项',
            'class': 'form-control input-lg',
        }),
        }
        error_messages = {
            'text': {'required': EMPTY_ERROR_MESSAGE}
        }
    # pass