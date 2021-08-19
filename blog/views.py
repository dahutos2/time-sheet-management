# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView
import datetime
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .models import Post, User
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .forms import SimpleScheduleForm
from .forms import SignUpForm
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.generic.edit import UpdateView

class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="registration/index.html"
    model = Post
    
    def get_queryset(self):
        query_set = Post.objects.filter(
            name=self.request.user).order_by('-date')
        
        return query_set
 
class Complite(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="blog/post_complite.html"
    model = Post
    
    def post(self, request):
        post = Post.objects.filter(name=request.user).update(published=False)
        print(request.user,'が完了しました。')
        
        return redirect('/')

class UserUpdate(UpdateView):
    template_name="registration/user_form.html"
    model = User
    fields = ["full_name","email"]
    success_url = "/"  
    
    def get(self, request, **kwargs):
        if not User.objects.get(id=self.kwargs['pk'])==request.user:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class IndexPost(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="blog/post_list.html"
    model = Post
    paginate_by = 10
    
    def get_queryset(self):
        query_set = Post.objects.filter(
            name=self.request.user).order_by('-date')
        
        return query_set
    
# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post
    
    def get(self, request, **kwargs):
        if not Post.objects.get(id=self.kwargs['pk']).name==request.user:
            return HttpResponse('不正なアクセスです。')
        if not Post.objects.get(id=self.kwargs['pk']).published:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class Update(UpdateView):
    model = Post
    fields = ["start_time", "end_time",]
    success_url = "/"
    
    def get(self, request, **kwargs):
        if not Post.objects.get(id=self.kwargs['pk']).name==request.user:
            return HttpResponse('不正なアクセスです。')
        if not Post.objects.get(id=self.kwargs['pk']).published:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    # 削除したあとに移動する先（トップページ）
    success_url = "/"
    
    def get(self, request, **kwargs):
        if not Post.objects.get(id=self.kwargs['pk']).name==request.user:
            return HttpResponse('不正なアクセスです。')
        if not Post.objects.get(id=self.kwargs['pk']).published:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

# CreateViewは新規作成画面を簡単に作るためのView
class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'blog/month_with_forms.html'
    model = Post
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request,self.template_name,context,)
    
    def post(self, request, **kwaegs):
        context = self.get_month_calendar()
        form_list = context['month_formset']
        forms = []
        for form in form_list:
            if form.is_valid():
                start_time = form.cleaned_data.get('start_time')
                end_time = form.cleaned_data.get('end_time')
                date = form.cleaned_data.get('date')
                if not (start_time and end_time) == None:
                    if Post.objects.filter(date=date, name=request.user).count() != 0:
                        context["helptext_day"] = '同じ日付の編集は編集画面で行なってください。'
                        return render(request,self.template_name,context)
                    elif int(start_time)>=int(end_time):
                        context["helptext_time"] = '指定時間が間違ってます。'
                        return render(request,self.template_name,context,)
                    else:
                        forms.append([start_time,end_time,date])
        for formset in forms:
            start_time = formset[0]
            end_time = formset[1]
            date = formset[2]
            Post.objects.create(start_time=start_time,
                                end_time=end_time,date=date,name=request.user)
                            
        return redirect('/')

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

