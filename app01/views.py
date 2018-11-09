import datetime

from django.shortcuts import render, redirect, HttpResponse

from app01.models import Book, Publish, Author, User
from app01.form import UserForm


# Create your views here.

def index(request):
    is_login = request.session.get("is_login")
    if not is_login:
        return redirect("/main/")
    """
    创建展示页面
    :param request:
    :return:
    """
    username = request.session.get("username")
    login_time = request.session.get("login_time")
    book_list = Book.objects.all()
    return render(request, "index.html", locals())


def add(request):
    is_login = request.session.get("is_login")
    if not is_login:
        return redirect("/main/")
        # return redirect("/login/")
    """
    添加页面
    :param request:
    :return:
    """
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        publish = request.POST.get("publish")
        pub_date = request.POST.get("pub_date")
        # getlist取出的数据是一个列表
        au_name = request.POST.getlist("au_name")
        print(au_name)
        # 在网页上获取的数据写到数据库中
        book = Book.objects.create(title=title, price=price, publish_id=publish, pub_date=pub_date)
        # 在Book_authors表中创建 book表和authors表之间的关联 多对多
        book.authors.add(*au_name)
        return redirect("/index/")
    else:
        pub_list = Publish.objects.all()
        au_list = Author.objects.all()
        return render(request, "add.html", {"pub_list": pub_list, "au_list": au_list})


def edit(request, id):
    is_login = request.session.get("is_login")
    if not is_login:
        return redirect("/main/")
        # return redirect("/login/")
    """
    创建编辑
    :param request:
    :param id:
    :return:
    """
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        publish = request.POST.get("publish")
        pub_date = request.POST.get("pub_date")
        au_name = request.POST.getlist("au_name")
        # 过滤id将其他修改
        Book.objects.filter(id=id).update(title=title, price=price, publish=publish, pub_date=pub_date)
        # 过滤id
        book_au = Book.objects.filter(id=id).first()
        # 将id添加到第三张表
        book_au.authors.set(au_name)
        return redirect('/index/')
    book_list = Book.objects.get(id=id)
    pub_list = Publish.objects.all()
    au_list = Author.objects.all()

    au_name = Book.objects.filter(id=id).first().authors.all().values_list("name")
    edit_author = []

    for i in au_name:
        edit_author.append(i[0])

    return render(request, "edit.html",
                  {"book_list": book_list, "pub_id": pub_list,
                   "au_list": au_list, "edit_author": edit_author}
                  )


def delbook(request, id):
    is_login = request.session.get("is_login")
    if not is_login:
        return redirect("/login/")
    # book = Book.objects.filter(id=id).first()
    # # # 删除关联表的记录
    # book.authors.clear()
    # Book.objects.filter(id=id).delete()

    return HttpResponse(str(id))


def registerandlogin1(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if User.objects.filter(user=user, pwd=pwd):
            obj = redirect("/index/")
            obj.set_cookie("is_login", True)
            obj.set_cookie("username", user)
            obj.set_cookie("login_time", datetime.datetime.now())
            print(obj)
            return obj

    return render(request, "registerandlogin.html")


def main(request):
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        if User.objects.filter(user=user, pwd=pwd):
            request.session["is_login"] = True
            request.session["username"] = user
            request.session["login_time"] = datetime.datetime.now().strftime('%Y/%m/%d %X')

            return redirect("/index/")
    return render(request, "registerandlogin.html")


def registerandlogin2(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print("############# success #############")
            print(form.cleaned_data)
            print(form.errors)
            user = request.POST.get("name")
            pwd = request.POST.get("pwd")
            print(user, pwd)
            user_list = User.objects.all().values("user")
            for name in user_list:
                if user == name['user']:
                    i_error = '您输入的用户名重复'
                    return render(request, "registerandlogin.html", locals())
            else:
                User.objects.create(user=user, pwd=pwd)

            return render(request, "registerandlogin.html")

        else:
            print("########### fail #########")
            print(form.cleaned_data)
            print(form.errors)
            print(type(form.errors))
            print(form.errors.get("email"))
            print(type(form.errors.get("email")))
            g_error = form.errors.get("__all__")
            if g_error:
                g_error = g_error[0]
            return render(request, "registerandlogin.html", locals())

    else:
        form = UserForm()
        return render(request, "registerandlogin.html", locals())


def logout(request):
    request.session.flush()
    return redirect('/main/')
    # return redirect('/login/')


def query(request):
    pass
