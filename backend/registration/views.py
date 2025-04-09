from django.shortcuts import render, redirect  # type: ignore
from registration.models import Registration
from django.db import IntegrityError  # type: ignore
from django.contrib import messages    # type: ignore

def index(request):
    if request.method == "POST":
        try:
            user_id = int(request.POST['id'])

            if user_id <= 0:
                 messages.error(request, "ID must be greater than 0.")
                 users = Registration.objects.all()
                 return render(request, 'registration/index.html', {
                    'users': users,
                    'old_data': request.POST
                })

            Registration.objects.create(
                id=user_id,
                name=request.POST['name'],
                email=request.POST['email'],
                phoneno=int(request.POST['phoneno']),
                date_of_birth=request.POST['dob']
            )

        except IntegrityError:
            messages.error(request, "User with this ID or Email already exists.")
            users = Registration.objects.all()
            return render(request, 'registration/index.html', {
                'users': users,
                'old_data': request.POST
            })

        return redirect('index')

    users = Registration.objects.all()
    return render(request, 'registration/index.html', {'users': users})


def delete_user(request, id):
    Registration.objects.get(id=id).delete()
    messages.success(request, f"User with ID {id} deleted.")
    return redirect('index')


def update_user(request, id):
    user = Registration.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phoneno = request.POST['phoneno']
        dob = request.POST['dob']

        user.name = name
        user.email = email
        user.phoneno = phoneno
        user.date_of_birth = dob

        try:
            user.save()
            return redirect('index')
        except IntegrityError:
            messages.error(request, "Email already exists! Please use a different one.")
            return render(request, 'registration/update.html', {
                'user': user,
                'old_data': {
                    'name': name,
                    'email': email,
                    'phoneno': phoneno,
                    'dob': dob
                }
            })

    return render(request, 'registration/update.html', {'user': user})
