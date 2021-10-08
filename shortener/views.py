from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from shortener.forms import RegisterForm
from shortener.models import Users

# Create your views here.

def index(request):
    print(request.user.pay_plan)
    print(request.user.is_superuser)
    user = Users.objects.filter(id=request.user.id).first()
    email = user.email if user else "Anonymous User!"

    print(email)
    print("Logged in?", request.user.is_authenticated)
    if request.user.is_authenticated is False:
        email = "Ananymous User!"
    print(email)
    return render(request, "base.html", {"welcome_msg": f"Hello {email}", "hello" : "world"})

@csrf_exempt
def get_user(request, user_id):
    print(user_id)
    if request.method == "GET":
        abc = request.GET.get("abc")
        xyz = request.GET.get("xyz")
        user = Users.objects.filter(pk=user_id).first()
        return render(request, "base.html", {"user": user, "params": [abc, xyz]})
    elif request.method == "POST":
        username = request.GET.get("username")
        if username:
            user = Users.objects.filter(pk=user_id).update(username=username)

        return JsonResponse(status=201, data=dict(msg="You just reached with Post Method!"), safe=False)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입 완료"
        return render(request, "register.html", {"form" : form, "msg" : msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form" : form})