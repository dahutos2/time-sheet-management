# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView
import datetime
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .models import Post, User
from django.urls import reverse_lazy
import datetime
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .forms import SimpleScheduleForm
from .forms import SignUpForm
from django.views.generic.edit import CreateView

from django.views.generic import TemplateView
#from .forms import activate_user

# ListViewは一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post

from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ["date", "start_time", "end_time",]

from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post

    # 削除したあとに移動する先（トップページ）
    success_url = "/"

# CreateViewは新規作成画面を簡単に作るためのView
class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'blog/month_with_forms.html'
    model = Post
    date_field = 'date'
    form_class = SimpleScheduleForm
        
    def get(self,request, **kwargs):
        context = self.get_month_calendar()
        return render(request,self.template_name,context,)
        
    def post(self,request, **kwargs):
        start_time = request.POST.get('start_time',False)
        end_time = request.POST.get('end_time',False)
        date = request.POST.get('date',)
        if start_time:
            if end_time:
                context = {date:(start_time,end_time)}
                context_qs = context.save(commit=False)
                context_qs.user_id = request.user_id
                context_qs.save()

        return redirect('/blog/',)
        
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ActivateView(TemplateView):
    template_name = "registration/activate.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        # 認証トークンを検証して、
        result = activate_user(uidb64, token)
        # コンテクストのresultにTrue/Falseの結果を渡します。
        return super().get(request, result=result, **kwargs)
