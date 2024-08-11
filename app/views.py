from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Community, Post, ChatMessage
from .forms import PostForm, ChatMessageForm
from .models import HelpSeek
from .forms import HelpSeekForm
from django.http import JsonResponse
import google.generativeai as genai

# Configure your API key
api_keyy = 'AIzaSyASQ7ympO59FqgN5VmHrMVz0jndRg31dnI'
genai.configure(api_key=api_keyy)
model = genai.GenerativeModel("gemini-pro")


def get_response(quest):
    help_topics = """Information on any disaster management, Safety rules to follow during a disaster, About us and any other related topics."""
    about = """This website was developed by a group of brilliant programmers called CherryPy. This website focuses on educating people on disaster readiness, response, and management."""
    prompt = f"""We have created a website that focuses on disaster management and information supplying. You are a chatbot we have used for the website.
    Keep in mind to give short strict responses that are 1 paragraph long. If the user asks a question unrelated to disaster management, respond by
    saying 'Sorry I will not be able to answer your question. I can help you with topics like: {help_topics}'. And about us you can say {about}. Also, remember to
    provide appropriate responses to greetings and goodbyes when the user greets you. The chatbot (your) name is Suraksha.
    The question asked by the user is: {quest}."""

    try:
        chat = model.start_chat()
        response = chat.send_message(prompt, stream=True)
        final_response = ""
        for chunk in response:
            final_response += chunk.text + "\n"
        return final_response.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"


def Weather(request):
    return render(request, 'weather.html')

def Contacts(request):
    return render(request, 'contacts.html')


def ask_chatbot(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_question = data.get('question')
        bot_response = get_response(user_question)
        return JsonResponse({'response': bot_response})
    return JsonResponse({'response': 'Invalid request method'}, status=400)


def dataH(request):
    return render(request, 'data.html')

def Elearn(request):
    return render(request, 'elearn.html')


def HeatMap(request):
    return render(request, 'map.html')


def seek_help(request):
    if request.method == 'POST':
        form = HelpSeekForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seekers')
    else:
        form = HelpSeekForm()
    return render(request, 'seek_help.html', {'form': form})


def seekers(request):
    seekers_list = HelpSeek.objects.all()
    return render(request, 'seekers.html', {'seekers_list': seekers_list})


def give_help(request, pk):
    seeker = HelpSeek.objects.get(pk=pk)
    return render(request, 'give_help.html', {'seeker': seeker})


@login_required
def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})


@login_required
def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    is_member = request.user in community.members.all()
    posts = community.posts.all().order_by('-created_at')
    chats = community.chats.all().order_by('-created_at')

    if request.method == 'POST':
        if 'post_form' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.community = community
                post.save()
                return redirect('community_detail', community_id=community.id)
        elif 'chat_form' in request.POST:
            chat_form = ChatMessageForm(request.POST)
            if chat_form.is_valid():
                chat_message = chat_form.save(commit=False)
                chat_message.user = request.user
                chat_message.community = community
                chat_message.save()
                return redirect('community_detail', community_id=community.id)
    else:
        post_form = PostForm()
        chat_form = ChatMessageForm()

    return render(request, 'community_detail.html', {
        'community': community,
        'posts': posts,
        'chats': chats,
        'post_form': post_form,
        'chat_form': chat_form,
        'is_member': is_member,
    })


@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.members.all():
        return redirect('community_detail', community_id=community.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.community = community
            post.save()
            return redirect('community_detail', community_id=community.id)
    return redirect('community_detail', community_id=community.id)


@login_required
def create_chat_message(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.members.all():
        return redirect('community_detail', community_id=community.id)

    if request.method == 'POST':
        form = ChatMessageForm(request.POST, request.FILES)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.community = community
            chat_message.save()
            return redirect('community_detail', community_id=community.id)
    return redirect('community_detail', community_id=community.id)


@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user not in community.members.all():
        community.members.add(request.user)
    return redirect('community_detail', community_id=community.id)


@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.user in community.members.all():
        community.members.remove(request.user)
    return redirect('community_detail', community_id=community.id)


def index(request):
    return render(request, 'welcome.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def home(request):
    communities = Community.objects.all()
    return render(request, 'home.html', {'communities': communities})


def logout(request):
    auth_logout(request)
    return redirect('login')
