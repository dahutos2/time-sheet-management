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
from .forms import SimpleScheduleForm, SignUpForm, SearchForm
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordContextMixin, FormView, TemplateView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _

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

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')

class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')
