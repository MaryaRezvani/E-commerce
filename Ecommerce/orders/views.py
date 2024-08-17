from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render,get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem, Coupon
from django.conf import settings
import requests
import json
import datetime
from django.contrib import messages

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart':cart})


class CartAddView(PermissionRequiredMixin, View):
    permission_required = 'orders.add_order'
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product,form.cleaned_data['quantity'])
        return redirect('orders:cart')


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order':order, 'form':self.form_class})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

        cart.clear()
        return redirect('orders:order_detail', order.id)




MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] ={
            'order_id':order.id,
        }
        req_data = {
            "MerchantID": MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }      
    # set content length by data
        headers = {'accept':'application/json','content-type': 'application/json'}
        req = requests.post(url=ZP_API_REQUEST, data= json.dumps(req_data), headers=headers)
        authority=req.json()['data']['authority']

        if len(req.json()['errors'])==0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"ERROR CODE:{e_code}, ERROR MESSAGE:{e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
             
            headers = {'accept':'application/json','content-type': 'application/json'}
            req_data = {
                "MerchantID": MERCHANT,
                "Amount": order.get_total_price(),
                "Authority": t_authority,
            }
            req = request.post(url = ZP_API_VERIFY, data= json.dumps(req_data), headers=headers)
            if len(req.json()['errors'])==0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.paid = True
                    order.save()
                    return HttpResponse('Transaction Success.\nRefID:'+str(
                        req.json()['data']['ref_id']))
                elif t_status == 101:
                    return HttpResponse('Transaction Submitted.\n'+str(
                        req.json()['data']['message']))
                else:
                    return HttpResponse('Transaction Failed.\nStatus:'+str(
                        req.json()['data']['message']))
                
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f'Errors code:{ e_code}, Errors message:{e_message}')
        else:
            return HttpResponse('Transaction failed or canceled by user')
        

class CouponApplyView(LoginRequiredMixin,View):
    form_class = CouponApplyForm
    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_form__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exist', 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)






