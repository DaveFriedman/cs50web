from django import forms


class entry_form(forms.Form):

    title = forms.CharField(label="Title", initial="title")
    body = forms.CharField(
        label="Body", 
        widget=forms.Textarea(attrs={"style": "height:50%; width:75%"})
        )