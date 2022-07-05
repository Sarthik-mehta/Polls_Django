from optparse import Option
from django.shortcuts import render,redirect
from .models import Question,Choice
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please Login first to access home page.")
        return redirect('login')
    
    questions = Question.objects.all()
    count = len(Question.objects.filter(author=request.user))
    val = bool(count<5)
    return render(request,'index.html',{'questions':questions,'enable':val})

def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please Login first to access your profile.")
        return redirect('login')
    questions = Question.objects.filter(author=request.user)
    val = bool(len(questions)<5)
    return render(request,'profile.html',{'questions':questions,'enable':val})

def vote(request,pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    # if request.method == 'POST':
    #     inputvalue = request.POST['choice']
    #     selection_option = options.get(id=inputvalue)
    #     selection_option.vote += 1
    #     selection_option.save()
    return render(request,'vote.html',{'question':question, 'options':options})

def result(request,pk):
    question = Question.objects.get(id=pk)
    options = question.choices.all()
    if request.method == 'POST':
        inputvalue = request.POST['choice']
        selection_option = options.get(id=inputvalue)
        selection_option.vote += 1
        selection_option.save()

    return render(request,'result.html',{'question':question, 'options':options})

def create(request):
    if request.method == 'POST':
        ques = request.POST['question']
        createdQuestion = Question(author=request.user,question = ques)
        createdQuestion.save()
        opt1 = request.POST['option1']
        opt2 = request.POST['option2']
        opt3 = request.POST['option3']
        opt4 = request.POST['option4']
        choice1 = Choice(question=createdQuestion,option=opt1,vote=0)
        choice1.save()
        choice2 = Choice(question=createdQuestion,option=opt2,vote=0)
        choice2.save()
        choice3 = Choice(question=createdQuestion,option=opt3,vote=0)
        choice3.save()
        choice4 = Choice(question=createdQuestion,option=opt4,vote=0)
        choice4.save()
        return redirect('index')

    return render(request,'create.html',{})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")