from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

user_names_recieved = []
def index(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        # if username in user_names_recieved:
        #     messages.error(request, 'username alerady taken please use another name')
        #     return HttpResponseRedirect(reverse('user'))
        # else:
        user_names_recieved.append(username)
        return render(request, "whiteboard.html", {'username': username , 'all_users': user_names_recieved})
    return HttpResponseRedirect(reverse('user'))

def user(request):
    return render(request, 'user.html')

    #
    # if request.method == 'POST':
    #     user.append(request.POST['user_name'])
    #     return HttpResponseRedirect(reverse('index'))
    # return HttpResponseRedirect(reverse('index'))