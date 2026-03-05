from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Category, Product, CartItem


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        slug = self.kwargs.get('slug')
        if slug:
            queryset = queryset.filter(category__slug=slug)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            context['category'] = get_object_or_404(Category, slug=slug)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, response):
        result = super().form_valid(response)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return result


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f'Not enough stock for {product.name}.')
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'{product.name} quantity updated in cart.')
    else:
        if product.stock < 1:
            cart_item.delete()
            messages.warning(request, f'{product.name} is out of stock.')
        else:
            messages.success(request, f'{product.name} added to cart.')
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart_item.delete()
            messages.success(request, f'{cart_item.product.name} removed from cart.')
        elif quantity > cart_item.product.stock:
            messages.warning(request, f'Only {cart_item.product.stock} available for {cart_item.product.name}.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    return redirect('cart')
