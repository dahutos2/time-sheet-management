from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from django import forms
from .models import Post


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""
    class Meta:
        model = Post
        fields = ('start_time','end_time','date',)
        widgets = {
            'start_time': forms.Select,
            'end_time': forms.Select,
            'date': forms.HiddenInput,}
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","full_name","password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.save()
        return user

class SearchForm(forms.Form):
    startdate = forms.DateInput()
    enddate = forms.DateInput()

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル')
