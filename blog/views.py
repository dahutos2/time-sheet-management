# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView

from .models import Post
from .models import User
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import SignUpForm

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

from django.views.generic.edit import CreateView

# CreateViewは新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Post

    # 編集対象にするフィールド
    fields = ["title", "body", "category", "tags",]

from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags",]

from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post

    # 削除したあとに移動する先（トップページ）
    success_url = "/"

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
