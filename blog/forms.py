from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
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
        
        help_text = {
            'username': '従業員番号を入力してください。',
            'password1': ('パスワードは最低 8 文字以上必要です。',
                       'パスワードを他の個人情報と類似させすぎてはなりません。',
                       'パスワードは、一般的に使用されるパスワードにすることはできません。',
                       'パスワードを完全に数値にすることはできません。'),}

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.save()
        return user
