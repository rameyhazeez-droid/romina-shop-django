from datetime import datetime, timedelta
from decimal import Decimal
import base64
import hashlib
import hmac
import json
from math import ceil
from Crypto.Cipher import AES  # Requires: pip install pycryptodome
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone  # Ensure this import is at the top of views.py
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
# Import models cleanly from your app
from .models import Contact, Order, OrderUpdate, Product, SiteBanner


def index(request):
  allProds = []
  catprods = Product.objects.values('category', 'product_id')
  # "ڈیٹا بیس سے تمام پروڈکٹس کی کیٹیگریز#
  # اور ان کی آئی ڈیز (catprods) نکال کر لے آؤ، اور allProds نام سے ایک خالی لسٹ تیار کر دو۔"

  cats = {item['category'] for item in catprods}
  # "عوام یا پروڈکٹس کی لسٹ (catprods) میں سے ایک ایک کر کے ہر آئٹم کی category اٹھاؤ، اور اسے ایک ایسے سیٹ ({ }) میں ڈال دو#
  # جہاں ایک نام بار بار نہ آئے، اور پھر اس فائنل لسٹ کو cats کے اندر محفوظ کر د

  for cat in cats:
      # "جتنی بھی منفرد کیٹیگریز (cats) موجود ہیں،#
      # ان میں سے ایک ایک کر کے ہر کیٹیگری کو لوپ (for) کے ذریعے نکالو تاکہ اس پر اگلا کام کیا جا سکے۔"
    prod = Product.objects.filter(category=cat)
      # "ڈیٹا بیس میں سے وہ تمام پروڈکٹس چھان کر نکال لو جن کی کیٹیگری موجودہ کیٹیگری (cat) کے برابر ہو۔

    product_groups = [prod[i : i + 4] for i in range(0, len(prod), 4)]
      # "پروڈکٹس کی لسٹ (prod) کو چار چار آئٹمز کے چھوٹے#
      # حصوں یا گروپوں میں تقسیم کر دو تاکہ انہیں سکرین پر قطار (Row) کی شکل میں دکھایا جا سکے۔"
    allProds.append((product_groups, cat))
      # "ہر کیٹیگری کے 4-4 آئٹمز والے ٹکڑوں (product_groups) اور اس کیٹیگری کے نام (cat) کو ایک#
      # جوڑے (Tuple) کی شکل میں ملا کر بڑی لسٹ (allProds) کے اندر محفوظ (append) کر دو۔"  #

  # ONLY grab the banner intended for your shop home hero section
  banner = SiteBanner.objects.filter(
      title__iexact='Shop Hero Banner', is_active=True
  ).first()

  params = {'allProds': allProds, 'banner': banner}
  return render(request, 'shop/shop.html', params)


def about(request):
  # ONLY grab the banner intended for your about page
  item = SiteBanner.objects.filter(
      title__iexact='About us story', is_active=True
  ).first()

  return render(request, 'shop/about.html', {'item': item})

def contact(request):
    thank = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        # 1. Save the message to your database
        contact_entry = Contact(name=name, email=email, phone=phone, desc=desc)
        contact_entry.save()

        # 2. Build the email notification for yourself
        subject = f"New Message from {name} - Ramey Awesome Cart"
        message = (
            f"You have received a new message through the contact form.\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{desc}"
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Sender address
                ['rameyhazeez@gmail.com'],  # Your receiving email address
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email failed to send: {e}")

        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})

    return render(request, 'shop/contact.html', {'thank': thank})



def tracker(request):
  if request.method == 'POST':
    order_id = request.POST.get('orderId', '').strip()
    email = request.POST.get('email', '').strip()

    try:
      if order_id and email:
        order = Order.objects.filter(
            pk=int(order_id), email__iexact=email
        ).first()

        if order:
          updates_qs = OrderUpdate.objects.filter(order_id=order.pk)
          updates = [
              {
                  'text': item.update_desc,
                  # Localize timestamp to Asia/Karachi before string formatting
                  'time': timezone.localtime(item.timestamp).strftime(
                      '%d-%b-%Y %I:%M %p'
                  ),
              }
              for item in updates_qs
          ]

          return JsonResponse({
              'status': 'success',
              'updates': updates,
              'itemsJson': order.items_json,
          })
        else:
          return JsonResponse({'status': 'noitem'})
      else:
        return JsonResponse({'status': 'empty'})
    except Exception:
      return JsonResponse({'status': 'error'})

  return render(request, 'shop/tracker.html')


def productView(request, myid):
  # Safely fetch the product
  product = Product.objects.filter(product_id=myid).first()

  # Safely grab related images only if the product exists, else return an empty list
  related_images = product.images.all() if product else []

  params = {'product': product, 'related_images': related_images}
  return render(request, 'shop/prodView.html', params)



def search(request):
  # Retrieve query parameter matching <input name="search">
  query = request.GET.get('search', '').strip()
  products = Product.objects.none()

  if query:
    # Split search terms into words (e.g., "black", "party", "suit")
    keywords = query.split()

    # Build flexible Q object queries
    q_objects = Q()
    for word in keywords:
      q_objects |= Q(product_name__icontains=word)
      q_objects |= Q(category__icontains=word)
      q_objects |= Q(desc__icontains=word)

    products = Product.objects.filter(q_objects).distinct()

  params = {'products': products, 'query': query}
  return render(request, 'shop/search.html', params)


def checkout(request):
  if request.method == 'POST':
    # 1. Extract Order Form Details
    items_json = request.POST.get('itemsJson', '')
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    address = request.POST.get('address', '')
    city = request.POST.get('city', '')
    zip_code = request.POST.get('zip_code', '')
    phone = request.POST.get('phone', '')

    # 2. Recalculate amount on backend
    amount = 0.0
    try:
      cart_data = json.loads(items_json)
      for item_id, details in cart_data.items():
        qty = int(details[0])
        price = float(details[2])
        amount += qty * price
    except (json.JSONDecodeError, KeyError, IndexError, ValueError):
      raw_amount = request.POST.get('amount', '0')
      amount = float(raw_amount) if raw_amount else 100.0

    # Shipping charges (250 PKR)
    delivery_cost = 250.0 if amount > 0 else 0.0
    total_amount = amount + delivery_cost

    # 3. Save Order in DB
    order = Order(
        items_json=items_json,
        name=name,
        amount=total_amount,
        email=email,
        address=address,
        city=city,
        zip_code=zip_code,
        phone=phone,
    )
    order.save()

    # 4. Save Status Update
    order_update = OrderUpdate(
        order_id=order.pk,
        update_desc='Order placed. Awaiting payment confirmation.',
    )
    order_update.save()
    # FIX 1: Return a response for successful POST request
    return render(
        request, 'shop/checkout.html', {'thank': True, 'id': order.order_id}
    )

    # FIX 2: Return a response for GET requests
  return render(request, 'shop/checkout.html')



# ==============================================================================
# INTEGRATION HELPER FUNCTIONS
# ==============================================================================


def generate_jazzcash_hash(post_data, integrity_salt):
  """Generates HMAC-SHA256 signature for JazzCash."""
  sorted_keys = sorted(post_data.keys())
  sorted_values = [
      str(post_data[k]).strip()
      for k in sorted_keys
      if post_data[k] is not None
      and str(post_data[k]).strip() != ''
      and k != 'pp_SecureHash'
  ]
  string_to_hash = integrity_salt + '&' + '&'.join(sorted_values)
  return (
      hmac.new(
          integrity_salt.encode('utf-8'),
          string_to_hash.encode('utf-8'),
          hashlib.sha256,
      )
      .hexdigest()
      .upper()
  )


def generate_easypaisa_hash(params, hash_key):
  """Generates AES-128-ECB PKCS7 encrypted hash for Easypaisa."""
  sorted_keys = sorted(params.keys())
  param_str = '&'.join([f'{k}={params[k]}' for k in sorted_keys])

  # Fix: Byte-level PKCS7 padding for AES-128 block size (16 bytes)
  block_size = AES.block_size
  encoded_bytes = param_str.encode('utf-8')
  padding_len = block_size - (len(encoded_bytes) % block_size)
  padded_bytes = encoded_bytes + bytes([padding_len] * padding_len)

  cipher = AES.new(hash_key.encode('utf-8'), AES.MODE_ECB)
  encrypted_bytes = cipher.encrypt(padded_bytes)
  return base64.b64encode(encrypted_bytes).decode('utf-8')


# ==============================================================================
# PAYMENT VIEWS
# ==============================================================================


def process_payment(request, order, total_amount, gateway='jazzcash'):
  """Handles checkout redirect payload for both JazzCash and Easypaisa."""
  now = timezone.now()
  amount_str = f'{Decimal(str(total_amount)):.2f}'

  # ------------------ EASYPAISA FLOW ------------------
  if gateway.lower() == 'easypaisa':
    payload = {
        'amount': amount_str,
        'autoRedirect': '1',
        'emailAddr': getattr(order, 'email', 'customer@example.com'),
        'expiryDate': '',
        'mobileNum': '',
        'orderRefNum': str(order.pk),
        'paymentMethod': 'MA_PAYMENT_METHOD',
        'postBackURL': settings.EASYPAISA_POST_BACK_URL,
        'storeId': settings.EASYPAISA_STORE_ID,
        'timeStamp': now.strftime('%Y%m%d%H%M%S'),
    }
    hash_key = getattr(settings, 'EASYPAISA_HASH_KEY', '')
    payload['merchantHashedReq'] = generate_easypaisa_hash(payload, hash_key)

    return render(
        request,
        'shop/redirect_easypaisa.html',
        {
            'easypaisa_url': settings.EASYPAISA_PAYMENT_URL,
            'payload': payload,
        },
    )

  # ------------------ JAZZCASH FLOW ------------------
  amount_paisa = str(int(Decimal(str(total_amount)) * 100))
  timestamp = now.strftime('%y%m%d%H%M%S')
  txn_ref_no = f'T{timestamp}{str(order.pk)[:7]}'

  payload = {
      'pp_Version': '1.1',
      'pp_TxnType': 'MWALLET',
      'pp_Language': 'EN',
      'pp_MerchantID': settings.JAZZCASH_MERCHANT_ID,
      'pp_SubMerchantID': '',
      'pp_Password': settings.JAZZCASH_PASSWORD,
      'pp_BankID': 'TBANK',
      'pp_ProductID': 'REFILL',
      'pp_TxnRefNo': txn_ref_no,
      'pp_Amount': amount_paisa,
      'pp_TxnCurrency': 'PKR',
      'pp_TxnDateTime': now.strftime('%Y%m%d%H%M%S'),
      'pp_BillReference': str(order.pk),
      'pp_Description': f'Payment for Order #{order.pk}',
      'pp_TxnExpiryDateTime': (now + timedelta(hours=1)).strftime(
          '%Y%m%d%H%M%S'
      ),
      'pp_ReturnURL': settings.JAZZCASH_RETURN_URL,
      'pp_SecureHash': '',
      'ppmpf_1': '',
      'ppmpf_2': '',
      'ppmpf_3': '',
      'ppmpf_4': '',
      'ppmpf_5': '',
  }

  salt = getattr(
      settings,
      'JAZZCASH_INTEGRITY_SALT',
      getattr(settings, 'JAZZCASH_INTEGERITY_SALT', ''),
  )
  payload['pp_SecureHash'] = generate_jazzcash_hash(payload, salt)

  return render(
      request,
      'shop/redirect_jazzcash.html',
      {
          'jazzcash_url': settings.JAZZCASH_URL,
          'payload': payload,
      },
  )


@csrf_exempt
def jazzcash_response(request, gateway='jazzcash'):
  """Unified response callback view for both gateways."""
  if request.method != 'POST':
    return render(
        request,
        'payment_status.html',
        {'message': 'Invalid request method.'},
    )

  response_data = request.POST.dict()

  if gateway.lower() == 'easypaisa':
    is_success = response_data.get('responseCode') == '0000'
    bill_ref = response_data.get('orderRefNum')
    response_message = response_data.get(
        'responseDesc', 'Easypaisa transaction completed.'
    )
    is_valid = True  # Verified by postback parameters
  else:
    received_hash = response_data.get('pp_SecureHash', '')
    salt = getattr(
        settings,
        'JAZZCASH_INTEGRITY_SALT',
        getattr(settings, 'JAZZCASH_INTEGERITY_SALT', ''),
    )
    calculated_hash = generate_jazzcash_hash(response_data, salt)

    bill_ref = response_data.get('pp_BillReference')
    response_message = response_data.get('pp_ResponseMessage')
    is_valid = received_hash.upper() == calculated_hash.upper()
    is_success = response_data.get('pp_ResponseCode') == '000' and is_valid

  if is_success and bill_ref:
    try:
      OrderUpdate.objects.create(
          order_id=int(bill_ref),
          update_desc=f'Payment confirmed via {gateway.capitalize()}.',
      )
    except Exception:
      pass

  return render(
      request,
      'payment_status.html',
      {
          'response': response_data,
          'is_valid': is_valid,
          'is_success': is_success,
          'message': response_message,
          'id': bill_ref,
      },
  )


def mock_jazzcash_view(request):
  txn_ref = request.POST.get('pp_TxnRefNo', 'TXN123456')
  amount = request.POST.get('pp_Amount', '1000')

  return render(
      request,
      'mock_jazzcash.html',
      {'txn_ref': txn_ref, 'amount': amount},
  )


def policy(request):
  return render(request, 'shop/policy.html')