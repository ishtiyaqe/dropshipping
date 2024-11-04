from .models import *


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cart = add_to_carts.objects.filter(User_id = request.user.id).count()
        request.cart = cart
        response = self.get_response(request)
        return response

