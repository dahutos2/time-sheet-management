# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView
import datetime
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .models import Post, User, Shift
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from . import mixins
from .forms import SimpleScheduleForm, SignUpForm, SearchForm
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.utils.translation import ugettext_lazy as _
import csv
import io
import urllib
from .forms import CSVUploadForm

class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="registration/index.html"
    model = Post

    def get_queryset(self):
        query_set = Post.objects.filter(
            name=self.request.user).order_by('-date')

        return query_set

class Mypage(ListView):
    template_name = 'admin/mypage.html'
    model = User

    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('startdate', None),
            self.request.POST.get('enddate', None),
        ]
        request.session['form_value'] = form_value

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startdate = ''
        enddate = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            startdate = form_value[0]
            enddate = form_value[1]
        default_data = {'startdate': startdate,
                        'enddate': enddate,
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        context['date_range'] = ','.join([startdate,enddate])
        context['range']= '〜'.join([startdate,enddate])

        return context

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            return redirect('/dahutos-admin/')
        return super().get(request)

    def get_queryset(self):
        query_set = User.objects.filter(
            username__istartswith=244).order_by('-last_login')

        return query_set

class Complite(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="blog/post_complite.html"
    model = Post

    def post(self, request):
        post = Post.objects.filter(name=request.user).update(published=False)
        print(request.user,'がシフトを完了しました。')

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
        if not request.user.is_authenticated:
            return redirect('/')
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
        print(request.user,'がシフトを提出しました。')
        return redirect('/')

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ShiftImport(generic.FormView):
    """
    役職テーブルの登録(csvアップロード)
    """
    template_name = 'admin/import.html'
    success_url = '/dahutos-admin/'
    form_class = CSVUploadForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_name'] = 'csvdownload'
        return ctx

    def form_valid(self, form):
        """postされたCSVファイルを読み込み、役職テーブルに登録します"""
        csvfile = io.TextIOWrapper(form.cleaned_data['file'])
        reader = csv.reader(csvfile)
        for i,row in enumerate(reader):
            if i == 0:
                continue
            else:
                print(row[1],row[2],row[3],row[4])
                Shift.objects.create(time=row[1],
                                 time_range=row[2],
                                 date=row[3],
                                 name=User.objects.get(username=row[4])
                                 )
        return super().form_valid(form)

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            return redirect('/dahutos-admin/')
        return super().get(request)
