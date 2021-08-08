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
            'start_time': forms.Select(
                attrs={'width': 'auto'},
                ),
            'end_time': forms.Select(
                attrs={'width': 'auto'},
                ),
            'date': forms.HiddenInput,}
    def save(self):
        super.clean()
        date = self.cleaned_data['date']
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        
        return date, start_time, end_time
        
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","full_name","password1", "password2")
        
        password1= forms.CharField(
            help_text=('パスワードは最低 8 文字以上必要です。',
                       'パスワードを他の個人情報と類似させすぎてはなりません。',
                       'パスワードは、一般的に使用されるパスワードにすることはできません。',
                       'パスワードを完全に数値にすることはできません。'))

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.save()
        return user


#    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
#        user = super().save(commit=False)
#        user.email = self.cleaned_data["email"]

        # 確認するまでログイン不可にする
#        user.is_active = False

#        if commit:
#            user.save()
#            activate_url = get_activate_url(user)
#            message = message_template + activate_url
#            user.email_user(subject, message)
#        return user

#def activate_user(uidb64, token):
    #try:
        #uid = urlsafe_base64_decode(uidb64).decode()
        #user = User.objects.get(pk=uid)
    #except Exception:
        #return False

    #if default_token_generator.check_token(user, token):
        #user.is_active = True
        #user.save()
        #return True

    #return False
