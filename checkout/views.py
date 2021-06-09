import json

import stripe
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from cart.models import Order, Cart
from . models import BillingForm, BillingAddress
from django.views.generic.base import TemplateView
from django.utils.datastructures import MultiValueDict as MVD
from .forms import NameForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY 


def checkout(request):


    # Checkout view
    form = BillingForm
    test_form = NameForm

    if request.method == "POST":
	    print(dict(request.POST), 'checkout')

    order_qs = Order.objects.filter(user= request.user, ordered=False)

    order_items = order_qs[0].orderitems.all()
    order_total = round(order_qs[0].get_totals(),0)
 
    


    context = {"form": form, "order_items": order_items, "order_total": order_total}
    print(str(context))
    # Getting the saved saved_address
    saved_address = BillingAddress.objects.filter(user = request.user)
    if saved_address.exists():
        savedAddress = saved_address.first()
        context = {"form": form, "order_items": order_items, "order_total": order_total,  "test_form": test_form}
    
        order_item = []
        str_s = ''
        for key, item in enumerate(order_items):
            str_s += str(item) + '; '
            # order_itm.append(str(item))

        with open('doc/order_items.json', 'w') as file:
            file.write(json.dumps({'order_items': str_s}))

        order_price= []
        with open('doc/order_total.json', 'w') as file:
            file.write(json.dumps({'order_total': order_total}))


    if request.method == "POST":
        saved_address = BillingAddress.objects.filter(user = request.user)
        print(dict(request.POST), 'checkout 2')
        if saved_address.exists():

            savedAddress = saved_address.first()
            form = BillingForm(request.POST, instance=savedAddress)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
        else:
            form = BillingForm(request.POST)
            if form.is_valid():
                billingaddress = form.save(commit=False)
                billingaddress.user = request.user
                billingaddress.save()
                
    return render(request, 'checkout/index.html', context)
    print(str(context))
from django.core.mail import send_mail


# import textwrap
# import smtplib

# def sendMail(FROM,TO,SUBJECT,TEXT,SERVER):
    
#     """this is some test documentation in the function"""
#     message = textwrap.dedent("""\
#         From: %s
#         To: %s
#         Subject: %s
#         %s
#         """ % (FROM, ", ".join(TO), SUBJECT, TEXT))
#     # Send the mail
#     server = smtplib.SMTP(SERVER)
#     server.sendmail(FROM, TO, message)
#     server.quit()

from django.shortcuts import redirect
from django.template import Template, Context
from docx import Document
from lxml import etree
from docxtpl import DocxTemplate



def create_document_email(email_addr, name):
    with open('doc/document.xml') as f:
        template_text = f.read()
    template = Template(template_text)

    with open('doc/order_items.json', 'r', encoding="utf-8") as file:
        order_items_info = json.loads(file.read())

    with open('doc/order_total.json', 'r', encoding="utf-8") as file:
        order_total_info = json.loads(file.read())

    email_addr = '005.ru'
    doc = DocxTemplate("doc/шаблон.docx")
    info = {'name': 'Коммерческое предложение', 'Title': order_items_info['order_items'],
            'цена': order_total_info['order_total'],
            'director': name, 'email ': email_addr}
    doc.render(info)
    doc.save("doc/kp.docx")
#     destination_document = Document('doc/document.docx')

    # with open('doc/document.xml') as f:
    #     template_text = f.read()
    # template = Template(template_text)
    #
    # text = 'Коммерческое предложение'
    # with open('doc/order_items.json', 'w', encoding="utf-8") as file:
    #     order_items_info = json.loads(file.read())
    #
    # with open('doc/order_total.json', 'w', encoding="utf-8") as file:
    #     order_total_info = json.loads(file.read())
    #
    # email_addr = '005.ru'
    # doc = DocxTemplate("doc/шаблон.docx")
    # context = {'ПРЕДЛОЖЕНИЕ': text, 'Title': order_items_info['order_items'],
    #            'цена': order_total_info['order_total'],
    #            'director': name, 'email ': email_addr}
    # doc.render(context)
    # doc.save("doc/шаблон-final.docx")

    # template_xml = template.render(Context({'Title': name, 'text':text, 'email': email_addr}))
    # template_xml = template.render(Context({'Title': name, 'abzac':text, 'Email': email_addr}))
    # target_xml_tree = etree.fromstring(template_xml.encode('utf-8'))
    # target_xml_tree = etree.fromstring(template_xml.encode('ascii'))
    # target_body = target_xml_tree[0]
    # root = destination_document._element
    # root.replace(root.body, target_body)
    # destination_document.save('doc/test.docx')

    #New docx
    # doc = DocxTemplate("doc/шаблон.docx")
    # context = {'emitent': 'name', 'Title': 'email'}
    # doc.render(context)
    # doc.save("doc/шаблон-final.docx")

# import mimetypes
# content_type = mimetypes.guess_type(instance.presentation.name)[0]


# Новая вьюха
from django.core.mail import EmailMessage
def send_email(request):
    if request.method == "POST":
        print(dict(request.POST), 'send')

        name = request.POST.get("name")
        # sendMail('and444petr@gmail.com', 'av269van@gmail.com', "Тест",  )
        # send_mail('Subject here', 'Here is the message.', 'from@example.com',
        # ['av269van@gmail.com'], fail_silently=False)

        # email = request.POST.get('email', '')

        # Куда отправлять для теста
        email = request.user.email
        #email = '005ark@gmail.com'
      
        #email = request.POST.get(email, '005ark@gmail.com')
      
        print(email)

        

        create_document_email('testt_email@ghgdh.com', name)

        # template_name = 'emailattachment.html'

        subject = 'Заказ от типографии 005.ru'
        message = 'Спасибо, что Вы с нами'

        # mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])





        # filename, content and mimetype. filename is the name of the file attachment as it will appear 
        # in the email, content is the data that will be contained inside the attachment and mimetype is 
        # the optional MIME type for the attachment. If you omit mimetype, the MIME content type will be 
        # guessed from the filename of the attachment.

        # message.attach('design.png', img_data, 'image/png')
        # (filename, content, mimetype)

        content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

        # with open('test.docx', encoding='utf-8') as f:
        with open('doc/kp.docx', 'rb') as f:
            mail.attach('kp.docx', f.read(), content_type)
        mail.send()
    else:
        pass


    return redirect("checkout:index")

def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user= request.user, ordered=False)
    order_total = order_qs[0].get_totals() 
    totalCents = float(order_total * 100);
    total = round(totalCents, 2)
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=total,
            currency='usd',
            description=order_qs,
            source=request.POST['stripeToken'])
        print(charge)
        
    return render(request, 'checkout/payment.html', {"key": key, "total": total})



# def demonstration_clusters(request):
#     if request.method == "POST":
#         left_user_id = request.POST.get("name1")
def charge(request):

    order = Order.objects.get(user=request.user, ordered=False)
    orderitems = order.orderitems.all()
    order_total = order.get_totals()
    print()
    totalCents = int(float(order_total * 100))

    if request.method == 'POST':
        # print(dict(request.POST) , ' gg')
        # charge = stripe.Charge.create(amount=totalCents,
        #     currency='inr',
        #     description=order,
        #     source=request.POST['stripeToken'])
        # print(charge)
        # if charge.status == "succeeded":

        orderId = get_random_string(length=16, allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        # print(charge.id)
        order.ordered = True
        # order.paymentId = charge.id
        order.orderId = f'#{request.user}{orderId}'
        order.save()
        cartItems = Cart.objects.filter(user=request.user)
        for item in cartItems:
            item.purchased = True
            item.save()
        return render(request, 'checkout/charge.html', {"items": orderitems, "order": order })



def oderView(request):
    print(dict(request.POST), ' gg')
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {
            "orders": orders
        }
    except:
        messages.warning(request, "У вас сейчас нет активного заказа")
        return redirect('/')
    return render(request, 'checkout/order.html', context)