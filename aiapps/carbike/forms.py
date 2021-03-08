from django import forms

class PhotoForm(forms.Form):
    image = forms.ImageField(
        label="image",
        widget=forms.FileInput(attrs={'class':'custom-file-input'}),
        required=False
    )

    # style = forms.ChoiceField(
    #     label='style',
    #     widget=forms.Select,
    #     # choices=LIBRARIES_CHOICES,
    #     required=True,
    # )

    style = forms.CharField(
        label='style',
        widget=forms.TextInput(attrs={'class':'style-input'}),
        max_length=50,
        required=True,
    )

    scraping = forms.CharField(
        label='scraping',
        widget=forms.TextInput(attrs={'class':'scraping-file-input'}),
        max_length=100,
        required=False
    )
    