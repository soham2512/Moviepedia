# from
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Movie.models import Movie, Rating

# Create your views here.

OMDB_API_KEY = 'ee61eeaf'


@login_required
def index(request):
    movie_data = Movie.objects.all().order_by('id')[0:10]
    continue_watching_data = Movie.objects.all().order_by('-id')
    top_rated_movie = Movie.objects.all().filter(Type='movie', imdbRating__gt=7).order_by('-imdbRating')[0:10]
    recently_released_movie = Movie.objects.all().filter(Type='movie', Year__gte=2022).order_by('-Year')[0:10]
    action_genre_movie = Movie.objects.all().filter(Type='movie', Genre__contains='Action' or 'Adventure')[0:10]

    rating_data = Rating.objects.all()
    our_db = True
    return render(request, "index.html", {'movie_data': movie_data,
                                          'continue_watching_data': continue_watching_data,
                                          'recently_released_movie': recently_released_movie,
                                          'top_rated_movie': top_rated_movie,
                                          'action_genre_movie': action_genre_movie,
                                          'our_db': our_db})


@login_required
def movieSearch(request):
    if request.method == "POST":
        query = request.POST.get('q')
        url = "http://www.omdbapi.com/?apikey=" + OMDB_API_KEY + "&s=" + query
        response = requests.get(url)
        print("------------------------")
        print(type(response))
        movie_data = response.json()
        print(movie_data)
        print(movie_data['Response'])

        if query:
            if movie_data['Response'] == 'True':
                movie_data = movie_data['Search']
                movie_api_result = True

                return render(request, "searchResult.html",
                              {'query': query, 'movie_data': movie_data, 'movie_api_result': movie_api_result})

            else:
                return render(request, "searchResult.html", {'query': query, 'movie_data': movie_data})



    else:
        return redirect("/movie")


@login_required
def movieDetails(request, imdbID):
    if Movie.objects.filter(imdbID=imdbID).exists():
        movie_data = Movie.objects.get(imdbID=imdbID)
        # print(movie_data.Poster)
        movie_rating_data = Rating.objects.filter(movie=movie_data)
        # print(movie_rating_data)

        our_db = True

        return render(request, "movieDetails.html",
                      {'movie_data': movie_data, 'movie_rating_data': movie_rating_data, 'our_db': our_db})



    else:
        url = "http://www.omdbapi.com/?apikey=" + OMDB_API_KEY + "&i=" + imdbID + "&plot=full"
        response = requests.get(url)
        movie_data = response.json()
        print(movie_data)
        movie_rating_data = movie_data['Ratings']
        print(movie_rating_data)

        # Inject to our database bellow:

        rating_objs = []

        # For the Rate
        for rate in movie_data['Ratings']:
            r, created = Rating.objects.get_or_create(source=rate['Source'], rating=rate['Value'])
            rating_objs.append(r)

        Poster_url = ''
        if movie_data['Poster'].lower() == 'n/a':
            Poster_url = 'https://raw.githubusercontent.com/soham2512/movie/main/login.jpg'
        else:
            Poster_url = movie_data['Poster']


        if movie_data['Type'] == 'movie':
                m, created = Movie.objects.get_or_create(
                    Title=movie_data['Title'],
                    Year=movie_data['Year'],
                    Rated=movie_data['Rated'],
                    Released=movie_data['Released'],
                    Runtime=movie_data['Runtime'],
                    Genre=movie_data['Genre'],
                    Actors=movie_data['Actors'],
                    Director=movie_data['Director'],
                    Writer=movie_data['Writer'],
                    Plot=movie_data['Plot'],
                    Language=movie_data['Language'],
                    Country=movie_data['Country'],
                    Awards=movie_data['Awards'],
                    Poster_url=Poster_url,
                    imdbRating=movie_data['imdbRating'],
                    imdbID=movie_data['imdbID'],
                    Type=movie_data['Type'],
                )

                m.Ratings.set(rating_objs)
                m.save()


        else:
            m, created = Movie.objects.get_or_create(
                Title=movie_data['Title'],
                Year=movie_data['Year'],
                Rated=movie_data['Rated'],
                Released=movie_data['Released'],
                Runtime=movie_data['Runtime'],
                Genre=movie_data['Genre'],
                Actors=movie_data['Actors'],
                Director=movie_data['Director'],
                Writer=movie_data['Writer'],
                Plot=movie_data['Plot'],
                Language=movie_data['Language'],
                Country=movie_data['Country'],
                Awards=movie_data['Awards'],
                Poster_url=Poster_url,
                imdbRating=movie_data['imdbRating'],
                imdbID=movie_data['imdbID'],
                Type=movie_data['Type'],
                totalSeasons=movie_data['totalSeasons'],

            )

            m.Ratings.set(rating_objs)
            m.save()

        our_db = False

        return render(request, "movieDetails.html",
                      {'movie_data': movie_data, 'movie_rating_data': movie_rating_data, 'our_db': our_db})
