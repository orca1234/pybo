from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserForm


def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pybo:index')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'common/signup.html', context)


@login_required(login_url='common:login')
def profile(request):
    """
    내 프로필
    """
    my_questions = request.user.author_question.all().order_by('-create_date')
    my_answers = request.user.author_answer.all().order_by('-create_date')
    context = {
        'my_questions': my_questions,
        'my_answers': my_answers,
    }
    return render(request, 'common/profile.html', context)