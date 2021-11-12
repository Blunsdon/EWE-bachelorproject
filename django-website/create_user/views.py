from django.shortcuts import render, redirect
from website.models import CreateUserCode
from website.forms import CreateNewUserForm

def create_user(request):
    """
    Home for create user
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            cu = request.POST.get('CreateUserCode')
            cuc = CreateUserCode.objects.get(id=1)
            if cu == cuc.code:
                form.save()
                return redirect('front_page')
    else:
        form = CreateNewUserForm()
    return render(request, "create_user.html", {'form': form})


