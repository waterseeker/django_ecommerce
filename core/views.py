from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from .forms import CheckoutForm
from django.utils import timezone


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            return redirect('core:checkout')
        messages.warning(self.request, "Failed checkout")
        return redirect('core:checkout')


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'


@login_required
def add_to_cart(request, slug):
    cart_item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=cart_item,
        user=request.user,
        ordered=False)
    order_query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query_set.exists():
        order = order_query_set[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=cart_item.slug).exists():
            order_item.order_quantity += 1
            order_item.save()
            messages.info(request, "Item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order_item.order_quantity = 1
            order_item.save()
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    cart_item = get_object_or_404(Item, slug=slug)
    order_query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query_set.exists():
        order = order_query_set[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=cart_item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=cart_item,
                user=request.user,
                ordered=False
            )[0]
            order_item.order_quantity = 0
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You don't have an active order.")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    cart_item = get_object_or_404(Item, slug=slug)
    order_query_set = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_query_set.exists():
        order = order_query_set[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=cart_item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=cart_item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.order_quantity > 1:
                order_item.order_quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You don't have an active order.")
        return redirect("core:product", slug=slug)
