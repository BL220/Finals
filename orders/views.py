from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from store.models import CartItem
from .models import Order, OrderItem
from .forms import OrderForm


# ──────────────────────────────────────────────
#  Class-Based View (Week 14 — CBV)
# ──────────────────────────────────────────────

class OrderHistoryView(LoginRequiredMixin, ListView):
    """Displays the logged-in user's order history."""
    model = Order
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')


# ──────────────────────────────────────────────
#  Function-Based View (checkout — complex logic)
# ──────────────────────────────────────────────

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                # Decrement stock
                item.product.stock -= item.quantity
                item.product.save()

            cart_items.delete()
            messages.success(request, f'Order #{order.pk} placed successfully!')
            return redirect('order_history')
    else:
        form = OrderForm()

    total = sum(item.subtotal for item in cart_items)
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })
