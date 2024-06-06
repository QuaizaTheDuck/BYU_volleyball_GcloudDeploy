from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from django.core.serializers import serialize
from .forms import ContactForm
from .models import ContactEntry,Mecze,Post,Zespol

def home_page(request):
    mecze = Mecze.objects.filter(data__gt=timezone.now()).order_by('data')
    mecze_json = serialize('json', mecze)

    # Znajdź najnowszy post oznaczony jako featured
    featured_post = Post.objects.filter(featured=True).order_by('-created_at').first()
    
    # Znajdź trzy najnowsze posty oznaczone jako latestnews
    latest_news = Post.objects.filter(latestnews=True).order_by('-created_at')[:4]

    # Zespol
    zespol = Zespol.objects.all()

    ostanieMecze = Mecze.objects.filter(Q(data__lt=timezone.now()) & ~Q(wynik=None)).order_by('-data')[:4]
    context = {
        'mecze': mecze,
        'mecze_json': mecze_json,
        'ostanieMecze' : ostanieMecze,
        'featured_post': featured_post,
        'latest_news': latest_news,
        'zespol': zespol
    }
    return render(request, 'main/home.html', context)


def faq_page(request):
    return render(request, 'main/faq.html')

def blog_page(request):
    # dodac ograniczenie na 16 postow maks 
    posts = Post.objects.order_by('-created_at')[:16]

    context = {
        'posts':posts
    }
    return render(request, 'main/blog.html', context)


def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Sprawdzenie, czy wszystkie pola formularza są uzupełnione
        if name and email and message:
            # Zapisanie wpisu do bazy danych
            contact = ContactEntry.objects.create(
                name=name,
                email=email,
                message=message
            )

            # Wysłanie maila
            send_mail(
                f"Message from {name} - {email}",
                message,
                email,
                ['quaiza.dev@gmail.com'],
            )

            # Przekierowanie użytkownika na stronę główną po wysłaniu formularza
            return redirect('home')
    else:
        # Jeśli metoda żądania nie jest POST, utwórz pusty formularz
        form = ContactForm()

    # Renderowanie szablonu z formularzem
    return render(request, 'main/contact.html', {'form': form})
