from typing import Optional

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from online_shop.forms import CommentModelForm, OrderModelForm, ProductModelForm
from online_shop.models import Product, Category, Comment


def product_list(request, category_slug: Optional[str] = None):
    categories = Category.objects.all().order_by('id')
    search = request.GET.get('q')
    filter_type = request.GET.get('filter', '')
    if category_slug:
        if filter_type == 'expensive':
            products = Product.objects.filter(category__slug=category_slug).order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.filter(category__slug=category_slug).order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(category__slug=category_slug) & Q(rating__gte=4)).order_by('-rating')

        else:
            products = Product.objects.filter(category__slug=category_slug)

    else:
        if filter_type == 'expensive':
            products = Product.objects.all().order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.all().order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(rating__gte=4)).order_by('-rating')
            print(products)

        else:
            products = Product.objects.all()

    if search:
        products = products.filter(Q(name__icontains=search) | Q(comments__name__icontains=search))

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'online_shop/home.html', context)


def product_detail(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product_id, is_provide=True).order_by('-id')
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    context = {
        'product': product,
        'comments': comments,
        'categories': categories,
        'related_products': related_products,
    }

    return render(request, 'online_shop/detail.html', context)


# def add_comment(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         body = request.POST.get('body')
#
#         comment = Comment(name=name, email=email, body=body)
#         comment.product = product
#         comment.save()
#
#         return redirect('product_detail', args=[product_id])
#
#     else:
#         pass
#
#     return render(request, 'online_shop/detail.html')


def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', product_id)

    else:
        form = CommentModelForm()

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'online_shop/detail.html', context)


def add_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm(request.POST)
    if request.method == 'GET':
        form = OrderModelForm(request.GET)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                product.save()
                order.save()
                messages.add_message(
                    request,
                    level=messages.SUCCESS,
                    message='Your order is successfully saved'
                )
                return redirect('product_detail', product_id)
            else:
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message='Your order is not available'
                )

    contex = {
        'form': form,
        'product': product,
    }
    return render(request, 'online_shop/detail.html', contex)


@login_required
def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {
        'form': form
    }

    return render(request, 'online_shop/add-product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id)

    return render(request, 'online_shop/edit-product.html', {'form': form})
