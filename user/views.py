from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from Movie.models import *
from Moviepedia import settings
from payment.models import *
from .tokens import generate_token


# Create your views here.

def publicIndex(request):
    movie_data = Movie.objects.all().order_by('id')[0:10]
    continue_watching_data = Movie.objects.all().order_by('-id')
    top_rated_movie = Movie.objects.all().filter(Type='movie', imdbRating__gt=7).order_by('-imdbRating')[0:10]
    recently_released_movie = Movie.objects.all().filter(Type='movie', Year__gte=2021).order_by('-Year')[0:10]
    action_genre_movie = Movie.objects.all().filter(Type='movie', Genre__contains='Action' or 'Adventure')[0:10]
    rating_data = Rating.objects.all()

    our_db = True
    return render(request, "publicIndex.html", {'movie_data': movie_data,
                                                'continue_watching_data': continue_watching_data,
                                                'recently_released_movie': recently_released_movie,
                                                'top_rated_movie': top_rated_movie,
                                                'action_genre_movie': action_genre_movie,
                                                'our_db': our_db})


def userSignup(request):
    print(request)
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')

        if User.objects.filter(username=username):
            messages.warning(request, "username is already taken, Try other.")
            return render(request, "sign-up.html")

        if User.objects.filter(email=email):
            messages.warning(request, "email is already registered.")
            return render(request, "sign-up.html")

        if len(username) > 10:
            messages.warning(request, "username is too long, Try other")
            return render(request, "sign-up.html")

        if len(password)<=5:
            messages.warning(request, "The length of password must be more than 5.")
            return render(request, "sign-up.html")

        # specialcharacters = ['!','@','#','$','%','^','&','*','(',')']
        # if password in specialcharacters == False:
        #     messages.warning(request, "Password must contain 1 special character.")
        #     return render(request, "sign-up.html")
        #
        # if [letter.isupper() for letter in password].count(True) < 1:
        #     messages.warning(request, "Password must contain 1 capital character.")
        #     return render(request, "sign-up.html")

        if password != repeatpassword:
            messages.warning(request, "Passwords do not match")
            return render(request, "sign-up.html")


        currentuser = User.objects.create_user(username=username,
                                               email=email,
                                               password=password)

        currentuser.first_name = firstname
        currentuser.last_name = lastname
        currentuser.is_active = False
        currentuser.save()

        messages.success(request, "Your account has been created.")
        messages.warning(request,
                         "Please visit the Link provided in the mail sent by moviepediamail@gmail.com to activate your account !!")

        # ------email confirmation link mail =========

        current_site = get_current_site(request)
        print(current_site)
        email_subject = "Hello " + currentuser.first_name + ". Confirm your email @ Moviepedia !!"

        email_message = render_to_string('email_confirmation.html', {
            'name': currentuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(currentuser.pk)),
            'token': generate_token.make_token(currentuser)
        })
        print(email_message)
        email = EmailMessage(
            email_subject, email_message,
            settings.EMAIL_HOST_USER, [currentuser.email],
        )
        email.fail_silently = True
        email.send()
        return redirect("/userLogin")

    return render(request, "sign-up.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated !!")
        return redirect("/userLogin")

    else:
        return render(request, "activation_failed.html")


def userLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/movie")

        elif request.user.is_active== False:
            messages.warning(request, "Your account is not activated yet.")
            messages.warning(request, "Please visit the Link provided in the mail sent by moviepediamail@gmail.com")
            messages.warning(request, "Make Sure to visit the Junk Folder in you mail.")
            return redirect("/userLogin")

        else:
            messages.warning(request, "Bad Credentials")
            return redirect("/userLogin")

    return render(request, "login.html")



def userDetails(request):
    if request.user.is_superuser:
        return redirect("/admin")

    else:
        user_data = {
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username
        }
        order_data = Order.objects.all().filter(username=request.user.username)
        order_data_length = len(order_data)
        return render(request, "setting.html", {'user_data': user_data, 'order_data_length': order_data_length})




def updateUser(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')

        if password != repeatpassword:
            messages.warning(request, "Passwords do not match")

        currentuser = request.user

        currentuser.first_name = firstname
        currentuser.last_name = lastname
        currentuser.set_password(password)
        currentuser.save()

        messages.success(request, "Your Details has been updated !! please Login Again")
    return render(request, "login.html")



def userLogout(request):
    logout(request)
    # messages.success(request, "You have been succesfully logged out.")
    # messages.warning(request, "Enter Username and Password to login again")
    return redirect("/")


def userOrders(request):
    # if request.user.is_superuser:
    #     return redirect("/admin")

    fullname = request.user.first_name + " " + request.user.last_name
    username = request.user.username
    order_data = Order.objects.all().filter(username=username)
    order_data_length = len(order_data)
    userOrderMovie = {}
    for order in order_data:
        userOrderMovie[order.transactionId] = Movie.objects.all().filter(imdbID=order.imdbID)

    movie_data = userOrderMovie.values()

    return render(request, "userOrders.html", {'movie_data': movie_data, 'order_data': order_data, 'fullname': fullname,
                                               'order_data_length': order_data_length, 'username': username})



    #
    # for ordermovie in order_imdbID:
    #     movie_data =
    #
    # print(movie)


def userOrderdetail(request, imdbID, username):
    movie_data = Movie.objects.filter(imdbID=imdbID)
    order_data = Order.objects.filter(imdbID=imdbID)
    user_data = {
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
        'username': request.user.username
    }
    return render(request, 'userOrderdetail.html',
                  {'movie_data': movie_data[0], 'order_data': order_data[0], 'user_data': user_data})
