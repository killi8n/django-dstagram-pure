from django.shortcuts import render

# Create your views here.
from accounts.forms import RegisterForm


def register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        register_form = RegisterForm()
    return render(request, 'registration/register.html', {'form': register_form})
