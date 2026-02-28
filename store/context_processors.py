from .models import CartItem, Category


def cart_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}


def categories_nav(request):
    return {'categories_nav': Category.objects.all()}
