from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, Post, Shift
from django import forms
import datetime as dt


class SimpleScheduleForm(forms.ModelForm):
    """シンプルなスケジュール登録用フォーム"""

    class Meta:
        model = Post
        fields = (
            "start_time",
            "end_time",
            "date",
        )
        widgets = {
            "start_time": forms.Select,
            "end_time": forms.Select,
            "date": forms.HiddenInput,
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "full_name", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.save()
        return user


class SearchForm(forms.Form):
    startdate = forms.DateInput()
    enddate = forms.DateInput()


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="CSVファイル")


class BS4ScheduleForm(forms.ModelForm):
    """Bootstrapに対応するためのModelForm"""

    class Meta:
        model = Shift
        fields = ("start_time", "end_time", "time", "description")
        widgets = {
            "start_time": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "end_time": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "time": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_end_time(self):
        start_time = self.cleaned_data["start_time"]
        end_time = self.cleaned_data["end_time"]
        if end_time <= start_time:
            if end_time > dt.time(hour=5):
                raise forms.ValidationError(
                    "終了時間は、開始時間よりも後にしてください"
                )
        return end_time
