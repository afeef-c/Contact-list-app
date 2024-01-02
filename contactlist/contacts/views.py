
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from . models import Contact
from django.contrib import messages
# Create your views here.

from django.http import HttpResponseForbidden

def superuser_required(view_func):
    """
    Decorator to require that the user is a superuser.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for '+ user)
            return redirect('userlogin')
    context = {'form':form}
    return render(request, 'contacts/register.html', context)

@never_cache
def login_user(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'username/password is incorrect !!')
            
        
    context = {}
    return render(request, 'contacts/user_login.html', context)


@never_cache
def login_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        username=request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'username/password is incorrect !!')
            
        
    context = {}
    return render(request, 'contacts/admin_login.html', context)


def logout_user(request):
    logout(request)
    return redirect('userlogin')

@login_required(login_url='userlogin')
def index(request):
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')

    if search_input:
        contacts = Contact.objects.filter(full_name__icontains = search_input)
    else:
        contacts = Contact.objects.all()
        search_input =''
    return render(request, 'contacts/index.html', {'contacts': contacts, 'search_input':search_input})

@superuser_required
@login_required(login_url='adminlogin')
def addContact(request):
    if request.method == 'POST':
        new_contact = Contact(
            full_name = request.POST['fullname'],
            relationship = request.POST['relationship'],
            email = request.POST['email'],
            phone_number = request.POST['phone-number'],
            address = request.POST['address'],
        )
        new_contact.save()
        return redirect('/')
    return render(request, 'contacts/new.html')


@login_required(login_url='userlogin')
def contactProfile(request, pk):
    contact = Contact.objects.get(id = pk)

    return render(request, 'contacts/contact_profile.html', {'contact': contact})

@superuser_required
@login_required(login_url='adminlogin')
def editContact(request, pk):
    contact = Contact.objects.get(id = pk)

    if request.method == 'POST':
        contact.full_name  = request.POST['fullname']
        contact.relationship  = request.POST['relationship']
        contact.email  = request.POST['email']
        contact.phone_number  = request.POST['phone-number']
        contact.address  = request.POST['address']
        contact.save()
        return redirect('/profile/'+ str(contact.id))
    return render(request, 'contacts/edit.html', {'contact': contact})


@superuser_required
@login_required(login_url='adminlogin')
def deleteContact(request, pk):
    contact = Contact.objects.get(id = pk)

    if request.method == 'POST':
        contact.delete()
        return redirect('/')
    return render(request, 'contacts/delete.html', {'contact':contact})


#====================================================
