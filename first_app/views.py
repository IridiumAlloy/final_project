from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Statute, Subsection, State
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['user'] = user.id
        return redirect("/welcome")
def welcome(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user']),
        'states': State.objects.all(),
    }
    return render(request, 'welcome.html', context)
def login(request):
    results= User.objects.filter(email=request.POST['email'])
    if len(results) == 0:
        messages.error(request,'email does not exist')
        redirect ('/')
    else:
        logged_in = results[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_in.password.encode()):
            request.session['user'] = logged_in.id
            return redirect ('/welcome')
        else:
            messages.error(request, "email and password do not match")
            return redirect ('/')
def logout(request):
    request.session.flush()
    return redirect('/')
def edit(request, user_id):
    if request.method == "POST":
        errors = User.objects.second_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/' + str(user_id))
        else:
            user = User.objects.get(id= user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
        return redirect('/edit/' + str(user_id))
    if request.method == 'GET':
        context = {
            "user": User.objects.get(id= request.session['user'])
        }
    return render(request,"edit_profile.html", context)
def user_page(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'edit_profile.html', context)
def legal_aid(request):
    context = {
        'user': User.objects.get(id=request.session['user']),
        'states': State.objects.all()
    }
    return render(request, "legal_aid.html", context)
def il_jca(request, statute_id):
    context = {
        'user': User.objects.get(id=request.session['user']),
        'statute': Statute.objects.get(id=statute_id),
        'subsections': Subsection.objects.filter(statutes= statute_id)
    }
    return render(request, 'iljca.html', context)
def add_subsection(request):
    if request.method == 'POST':
        results = Statute.objects.filter(name = request.POST['statute'])
        if len(results) == 0 :
            statute = Statute.objects.create(
                name = request.POST['statute'],
                states = State.objects.get(name=request.POST['state'])
            )
        else:
            statute = Statute.objects.get(name= request.POST['statute'])
        Subsection.objects.create(
            citation = request.POST['citation'],
            section = request.POST['section'],
            language = request.POST['language'],
            statutes = statute
        )
        return redirect ('/add_subsection')
    else:
        context = {
            "statutes": Subsection.objects.all()
        }
        return render(request, "add_statute.html", context)
def save_section(request, subsection_id):
    section = Subsection.objects.get(id= subsection_id)
    this_user = User.objects.get(id= request.session['user'])
    section.user_likes.add(this_user)
    return redirect('/welcome')
def saved_stat(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'saved.html', context)