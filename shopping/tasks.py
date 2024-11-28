from celery import shared_task
import stripe
from django.conf import settings
from .models import Product, OrderItem, AppUser

stripe.api_key = settings.STRIPE_SECRET_KEY

@shared_task
def process_order(user_id, items, success_url, cancel_url):
    try:
        user = AppUser.objects.get(id=user_id)
        line_items = []
        shipping_amount = 70  # Define a fixed shipping amount
        
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                user=user,
                product=product,
                quantity=item['quantity'],
                price=product.price,
            )

            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': item['product_name'],
                    },
                    'unit_amount': int(product.price * 100) + (shipping_amount * 100),
                },
                'quantity': item['quantity'],
            })

        # Create a Stripe Checkout Session with all the order items
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        return session.url

    except stripe.error.StripeError as e:
        return {'error': f'Stripe error: {str(e)}'}
    except Exception as e:
        return {'error': f'Error: {str(e)}'}
