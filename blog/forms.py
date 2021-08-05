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
        time_list=((1,'9:00'),(2,'10:00'),(3,'11:00'),(4,'12:00'),(5,'13:00'),
             (6,'14:00'),(7,'15:00',),(8,'16:00'),(9,'17:00'),(10,'18:00'),
             (11,'19:00'),(12,'20:00'),(13,'21:00'),(14,'22:00'),(15,'23:00'),
             (16,'24:00')
            )
        model = Post
        fields = ('start_time', 'end_time','date')
        widgets = {
            'start_time': forms.Select(
                choices=time_list,
                attrs={'class': 'form-control'},
                ),
            'end_time': forms.Select(
                choices=time_list,
                attrs={'class': 'form-control'},
                ),
            'date': forms.HiddenInput,
        }
        
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
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
