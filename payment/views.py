import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Movie.models import *
from payment.models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def orderDetails(request, imdbID):
    movie_data = Movie.objects.filter(imdbID=imdbID)
    if movie_data:
        print(movie_data)

        user_data = {
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username
        }
        print(user_data)

        return render(request, "orderDetails.html", {'movie_data': movie_data[0], 'user_data': user_data})


@csrf_exempt
def checkout(request, imdbID):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1KkaJmDgysOue1ArtR1qbMvQ',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            '/payment/thanks') + '?session_id={CHECKOUT_SESSION_ID}' + '&imdbID=' + imdbID,
        cancel_url=request.build_absolute_uri('/payment/orderDetails'),
    )

    return JsonResponse({
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def thanks(request):
    # movie_data = Movie.objects.filter(imdbID=imdbID)
    session = request.GET.get('session_id', '')
    imdbID = request.GET.get('imdbID', '')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = stripe.checkout.Session.list_line_items(session)
    print(line_items)
    line_items = line_items.data[0]
    o, created = Order.objects.get_or_create(
        imdbID=imdbID,
        username=request.user.username,
        email=request.user.email,
        amount=line_items['amount_total'],
        currency=line_items['currency'],
        transactionId=line_items['id'],

    )
    o.save()
    # orderData = Order.objects.filter('transactionId'=transactionId)
    movie_data = Movie.objects.filter(imdbID=imdbID)
    username = request.user.username
    print(movie_data)
    print(line_items)

    return render(request, 'thanks.html', {'line_items': line_items, 'movie_data': movie_data, 'username': username})

# stripe listen --forward-to localhost:8000/payment/stripe_webhook/
# @csrf_exempt
# def stripe_webhook(request):
#     # You can find your endpoint's secret in your webhook settings
#     endpoint_secret = 'whsec_ea3f0dd5092f9f44ecb9fdefcea530dd2d091562f9d46e0c8426ca9cc8bd0e81'
#
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
#
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)
#
#     # Handle the checkout.session.completed event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         print(session)
#         o, created = Order.objects.get_or_create(
#             username=request.user.username,
#             imdbID='tt',
#             amount=session['amount_total'],
#             currency=session['currency'],
#             email=session['customer_details'].email,
#             name=session['customer_details'].name,
#             transactionId=session['id'],
#             method=session['payment_method_types'][0],
#             status=session['payment_status'],
#             country=session['customer_details'].address.country,
#             postal=session['customer_details'].address.postal_code,
#         )
#         o.save()
#     return HttpResponse(status=200)
