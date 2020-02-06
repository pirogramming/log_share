from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
from .models import Profile

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password = request.POST["password"]
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request,'accounts/login.html',{'error':'login error'})
    else:
        return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


from .models import Profile


# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('posts:list')
#
#     if request.method == 'POST':
#         signup_form = UserCreationForm(request.POST)
#         if signup_form.is_valid():
#             user = signup_form.save()
#             Profile.objects.create(user=user)  # 프로필 생성
#             auth_login(request, user)
#             return redirect('posts:list')
#
#     else:
#         signup_form = UserCreationForm()
#
#     return render(request, 'accounts/signup.html', {'signup_form': signup_form})

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"])
            name = request.POST["name"]
            department=request.POST["department"]
            description=request.POST["description"]
            naver=request.POST["naver"]
            daum = request.POST["daum"]
            # photo=request.POST["photo"]
            github = request.POST["github"]
            profile = Profile(user=user, name=name,department=department,description=description,naver=naver,daum=daum,github=github)
            profile.save()
            auth.login(request,user)
            return redirect('/')
    return render(request, 'accounts/signup.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

