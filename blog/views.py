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
from .forms import CSVUploadForm, BS4ScheduleForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="registration/index.html"
    model = Post
    paginate_by = 5

    def get(self, request, **kwargs):
        help_user = User.objects.get(username=244)
        if request.user == help_user:
            return redirect('/shift/')
        return super().get(request)

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
            return redirect('/')
        return super().get(request)

    def get_queryset(self):
        query_set = User.objects.filter(
            username__istartswith=244).order_by('-last_login').exclude(username=244)

        return query_set

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

        ページングしたい場合に利用してください。

        countは、1ページに表示する件数です。
        返却するPgaeオブジェクトは、以下のような感じで使えます。

            {% if page_obj.has_previous %}
              <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
            {% endif %}

        また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。

    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


class UserShift(DetailView):
    template_name="admin/user_shift.html"
    model = User

    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('startdate', None),
            self.request.POST.get('enddate', None),
        ]
        request.session['form_value'] = form_value

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        startdate = ''
        enddate = ''
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        shift_objects = Shift.objects.filter(name=user).order_by('-date')
        post_objects = Post.objects.filter(name=user).order_by('-date')
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            startdate = form_value[0]
            enddate = form_value[1]
        default_data = {'startdate': startdate,
                        'enddate': enddate,
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        page_shift_obj = paginate_queryset(self.request, shift_objects, 1)
        page_post_obj = paginate_queryset(self.request, post_objects, 1)
        context['test_form'] = test_form
        context['date_range'] = ','.join([startdate,enddate])
        context['range']= '〜'.join([startdate,enddate])
        context['page_shift_obj'] = page_shift_obj
        context['page_post_obj'] = page_post_obj

        return context


    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            return redirect('/dahutos-admin/')
        return super().get(request)

class Complite(ListView,):
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
        help_user = User.objects.get(username=244)
        if request.user == help_user:
            return redirect('/shift/')
        return super().get(request)

class IndexPost(mixins.MonthCalendarMixin, ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    template_name="blog/index_post.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            context['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        help_user = User.objects.get(username=244)
        if request.user == help_user:
            return redirect('/shift/')
        return super().get(request)

class Update(UpdateView):
    model = Post
    fields = ["start_time", "end_time",]
    success_url = "/mypage/"

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            if not Post.objects.get(id=self.kwargs['pk']).name==request.user:
                return HttpResponse('不正なアクセスです。')
            if not Post.objects.get(id=self.kwargs['pk']).published:
                return HttpResponse('不正なアクセスです。')
        return super().get(request)

from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    # 削除したあとに移動する先（トップページ）
    success_url = "/mypage/"

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
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
        help_user = User.objects.get(username=244)
        if request.user == help_user:
            return redirect('/shift/')
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
        if forms == []:
            context["helptext_input"] = '未入力の部分があります。'
            return render(request,self.template_name,context,)
        else:
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
                if User.objects.filter(username=row[4]).exists():
                    start_time = row[2].split('〜')[0]
                    end_time = row[2].split('〜')[1]
                    end_time_min = int(end_time.split(':')[0])*60+int(end_time.split(':')[1])
                    start_time_min = int(start_time.split(':')[0])*60+int(start_time.split(':')[1])
                    time_min_old = end_time_min - start_time_min
                    time_min = int(time_min_old - float(row[1])*60)
                    time = datetime.time(hour=time_min//60,minute=time_min%60)
                    if int(end_time.split(':')[0]) >= 24:
                        end_time = (str(int(end_time.split(':')[0])-24)
                                    + ':' + end_time.split(':')[1])
                    date=row[3]
                    if row[4] == '244':
                        Shift.objects.create(time=time,
                           start_time=start_time,
                           end_time=end_time,
                           date=date,
                           name=User.objects.get(username=row[4])
                           )
                    elif not Shift.objects.filter(time=time,
                                 start_time=start_time,
                                 end_time=end_time,
                                 date=date,
                                 name=User.objects.get(username=row[4])
                                 ).exists():
                                 Shift.objects.create(time=time,
                                    start_time=start_time,
                                    end_time=end_time,
                                    date=date,
                                    name=User.objects.get(username=row[4])
                                    )
        return super().form_valid(form)

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            return redirect('/dahutos-admin/')
        return super().get(request)

class ShiftView(mixins.MonthCalendarMixin, ListView):
    template_name = 'blog/shift.html'
    model = Shift

    def get(self, request, **kwargs):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        help_user = User.objects.get(username=244)
        if year:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
            if not request.user == help_user:
                if Shift.objects.filter(date=date,name=request.user).exists():
                        objects = Shift.objects.filter(date=date,name=request.user)
                        pk = [object.id for object in objects][0]
                        return redirect('/shift/update/{}'.format(pk))

        if not request.user.is_authenticated:
            return redirect('/')
        return super().get(request)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            context['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        return context

class ShiftUpdate(mixins.MonthCalendarMixin, UpdateView):
    template_name = 'blog/shift_form.html'
    model = Shift
    form_class = BS4ScheduleForm
    success_url = "/shift/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            context['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        context['night_time'] = datetime.time(hour=5)
        return context

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            if not Shift.objects.get(id=self.kwargs['pk']).name==request.user:
                return HttpResponse('不正なアクセスです。')
        return super().get(request)

class ShiftDelete(DeleteView):
    model = Shift
    # 削除したあとに移動する先（トップページ）
    success_url = "/mypage/"

    def get(self, request, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class ShiftIndex(ListView):
        # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Shift
    template_name="blog/shift_index.html"
    paginate_by = 5

    def get_queryset(self):
        query_set = Shift.objects.filter(
            name=self.request.user).order_by('-date')

        return query_set

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
        context['range'] = '〜'.join([startdate,enddate])
        context['objects'] = Shift.objects.filter(
            name=self.request.user).order_by('-date')

        return context

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')
        help_user = User.objects.get(username=244)
        if request.user == help_user:
            return redirect('/shift/')
        return super().get(request)
