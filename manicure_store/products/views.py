from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView, DetailView
from django.core.mail import send_mail
from .forms import OrderForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail


# Create your views here.
# class IndexView(TemplateView):
#     template_name = 'products/index.html'
#
#     def get_context_data(self, **kwargs):
#         baskets = Basket.objects.filter(session=request.session.session_key)
#         context = super(IndexView, self).get_context_data()
#         context['title'] = 'NailStore'
#         context['baskets'] = baskets
#         return context


# class ContactsView(TemplateView):
#     template_name = 'products/contacts.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ContactsView, self).get_context_data()
#         context['title'] = 'Контакты'
#         return context


# class ProductsListView(ListView):
#     model = Product
#     template_name = 'products/products.html'
#     paginate_by = 15
#     title = 'NailStore - Каталог'
#
#     def get_queryset(self):
#         queryset = super(ProductsListView, self).get_queryset()
#         category_id = self.kwargs.get('category_id')
#         return queryset.filter(category_id=category_id) if category_id else queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductsListView, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         context['title'] = 'NailStore'
#         return context


def index(request):
    baskets = Basket.objects.filter(session=request.session.session_key)
    context = {'title': 'NailStore',
               'baskets': baskets
               }
    return render(request, 'products/index.html', context)


def contacts(request):
    baskets = Basket.objects.filter(session=request.session.session_key)
    context = {'title': 'Контакты',
               'baskets': baskets
               }
    return render(request, 'products/contacts.html', context)


#
def products(request, category_id=None, page=1):
    baskets = Basket.objects.filter(session=request.session.session_key)
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    per_page = 6
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    print('________________________________')
    print(request.session.session_key)
    print('________________________________')

    context = {'title': 'Nail Polish Store',
               'categories': Category.objects.all(),
               'products': products_paginator,
               'baskets': baskets,
               }
    return render(request, 'products/products.html', context)


def basket_views(request):
    baskets = Basket.objects.filter(session=request.session.session_key)
    total_sum = 0
    total_quantity = 0
    for basket in baskets:
        total_sum += basket.sum()
        total_quantity += basket.quantity
    context = {'title': 'Nail Polish Store',
               'baskets': baskets,
               'total_sum': total_sum,
               'total_quantity': total_quantity,
               'form': OrderForm
               }
    return render(request, 'products/baskets.html', context)


def basket_add(request, product_id):
    print('**********************')
    print(request.session.session_key)
    print('**********************')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(session=request.session.session_key, product=product)
    if not baskets.exists():
        Basket.objects.create(session=request.session.session_key, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    print('______________________')
    print(basket_id, '888888')
    print(basket)
    print('______________________')
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def send_data_mail(request):
    # form = OrderForm()
    # print(form)
    # print(form.is_valid())
    # print('............................')
    # print(form.errors)
    # print(form.non_field_errors)
    # print('............................')
    #
    #
    # if form.is_valid():
    #     context = {'text': "Ваш заказ принят. Мы свяжемся с Вами в скором времени."}
    # else:
    #     context = {'text': 'Пожалуйста, заполните форму корректно'}

    data = request.POST
    print(data)
    print('/////////////////////////')
    print(request.session.session_key)
    name = data.get('name')
    number = data.get('number')
    address = data.get('address')
    text = f'Имя: {name}\n' \
           f'Телефон: {number}\n' \
           f'Адрес доставки: {address}\n\n'
    baskets = Basket.objects.filter(session=request.session.session_key)
    for product in baskets:
        text += "Наименование: " + product.product.name + "\n" + 'Цена: ' + str(
            product.product.price) + "\n" + "Количество:" + str(product.quantity) + '\n\n'

    send_mail(
        'New order',
        text,
        'pshek8863@gmail.com',
        ['annexol@yandex.ru'],
        fail_silently=False,
    )
    # basket = Basket.objects.filter(session=request.session.session_key)
    # print(basket[0])
    # # Ordered.objects.create(product=)
    # User.objects.create(name=data.get('name'), address=data.get('address'), number=data.get('number'))
    print('/////////////////////////')
    request.session.create()
    # request.session.pop('oau6mljxnk20acuv32goewv817d0s6kv',None)
    # request.session.delete()
    # print(request.session.delete())

    return render(request, 'products/send.html',
                  context={'text': "Ваш заказ принят. Мы свяжемся с Вами в скором времени."})

# class ShorteningLink(SuccessMessageMixin, CreateView):
#     model = Links
#     form_class = AddLink
#     template_name = 'short/shortening_link.html'
#     success_url = reverse_lazy('shortening_link')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'shortening_link'
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = AddLink(request.POST)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         old_link = self.request.POST.get('your_link')
#         s = pyshorteners.Shortener()
#         new_link = s.tinyurl.short(old_link)
#         self.object = form.save(commit=False)
#         self.object.user_name = User.objects.all().filter(username=self.request.user)[0]
#         self.object.new_link = new_link
#         self.object.save()
#         self.success_message = new_link
#         return super().form_valid(form)
