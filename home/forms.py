from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        label="Your email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "you@example.com",
        })
    )

    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Your message or request",
        })
    )
