from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile
from .utils import fetch_news
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import SavedArticle
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CustomLoginForm
from django.views.generic import CreateView
from .forms import CustomSignupForm

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('preferences')

def home(request):
    articles = []
    paginated_articles = None  # Initialize the variable
    total_results = 0  # Track total number of results for pagination

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            page_number = request.GET.get('page', 1)  # Get current page number
            articles, total_results = fetch_news(profile.topics, page=page_number)  # Pass page number to fetch_news

            # Implement Django pagination using total results
            paginator = Paginator(range(total_results), 5)  # Total results and articles per page

            # Handle potential pagination errors
            try:
                paginated_articles = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_articles = paginator.page(1)
            except EmptyPage:
                paginated_articles = paginator.page(paginator.num_pages)

        except UserProfile.DoesNotExist:
            pass  # Handle case where user profile doesn't exist

    return render(request, 'news/home.html', {
        'articles': articles,
        'paginator': paginated_articles,  # Pass paginated object to template
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'news/signup.html', {'form': form})

def preferences(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage after saving preferences
    else:
        # Load the current preferences if they exist
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'news/preferences.html', {'form': form})


@login_required
def save_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        description = request.POST['description']
        SavedArticle.objects.create(
            user=request.user,
            title=title,
            url=url,
            description=description
        )
    return redirect('home')

@login_required
def saved_articles(request):
    articles = SavedArticle.objects.filter(user=request.user)
    return render(request, 'news/saved_articles.html', {'articles': articles})


@login_required
def remove_saved_article(request, article_id):
    saved_article = get_object_or_404(SavedArticle, id=article_id, user=request.user)
    saved_article.delete()
    return redirect('saved_articles')  # Redirect back to saved articles page

class CustomLoginView(LoginView):
    form_class = CustomLoginForm  # Set your custom form here

    def get_success_url(self):
        return reverse('preferences')
    
class SignupView(CreateView):
    form_class = CustomSignupForm
    template_name = 'signup.html'
    success_url = '/login/'  # Redirect to a success page after signup