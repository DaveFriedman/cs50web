from django import forms


class entry_form(forms.Form):

    title = forms.CharField(
        initial="title",
        label="Title",
        widget=forms.TextInput()
        )
    body = forms.CharField(
        label="Body",
        widget=forms.Textarea()
        )