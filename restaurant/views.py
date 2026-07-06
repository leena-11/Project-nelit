from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Category, MenuItem, Order, OrderItem
from .cart import Cart
import json

def home(request):
    categories = Category.objects.all()
    # Add count of items for each category
    for cat in categories:
        cat.item_count = cat.items.count()
    
    cart = Cart(request)
    return render(request, 'restaurant/home.html', {
        'categories': categories,
        'cart': cart,
    })

def menu(request):
    categories = Category.objects.all()
    selected_category_slug = request.GET.get('category', 'all')
    
    if selected_category_slug == 'all':
        items = MenuItem.objects.all()
    else:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        items = MenuItem.objects.filter(category=selected_category)
        
    cart = Cart(request)
    return render(request, 'restaurant/menu.html', {
        'categories': categories,
        'items': items,
        'selected_category': selected_category_slug,
        'cart': cart,
    })

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'restaurant/cart.html', {
        'cart': cart
    })

@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
        except:
            quantity = 1
        cart.add(menu_item=menu_item, quantity=quantity)
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': f"Added {menu_item.name} to cart"
        })
        
    # Standard POST fallback
    quantity = int(request.POST.get('quantity', 1))
    cart.add(menu_item=menu_item, quantity=quantity)
    return redirect('restaurant:menu')

@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity'))
            override = data.get('override', True)
        except:
            return JsonResponse({'success': False, 'error': 'Invalid request data'}, status=400)
            
        cart.add(menu_item=menu_item, quantity=quantity, override_quantity=override)
        
        # Calculate single item total
        item_total = 0
        for item in cart:
            if item['menu_item'].id == menu_item.id:
                item_total = item['total_price']
                break
                
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'item_total': float(item_total),
            'subtotal': float(cart.get_subtotal()),
            'gst': float(cart.get_gst()),
            'total': float(cart.get_total()),
        })
        
    # Standard POST fallback
    quantity = int(request.POST.get('quantity', 1))
    cart.add(menu_item=menu_item, quantity=quantity, override_quantity=True)
    return redirect('restaurant:cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart.remove(menu_item)
    
    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'subtotal': float(cart.get_subtotal()),
            'gst': float(cart.get_gst()),
            'total': float(cart.get_total()),
        })
        
    return redirect('restaurant:cart_detail')

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('restaurant:menu')
        
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        table_number = request.POST.get('table_number')
        special_instructions = request.POST.get('special_instructions', '')
        
        if customer_name and phone_number and table_number:
            # Create Order
            order = Order.objects.create(
                customer_name=customer_name,
                phone_number=phone_number,
                table_number=table_number,
                special_instructions=special_instructions,
                total_amount=cart.get_total()
            )
            
            # Create Order Items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item['menu_item'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect to tracking page
            return redirect(f"/track/?order_id={order.id}")
            
    return render(request, 'restaurant/checkout.html', {
        'cart': cart
    })

def track_order(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None
            
    return render(request, 'restaurant/track.html', {
        'order': order,
        'order_id': order_id
    })

def kitchen_dashboard(request):
    # Get all active orders (Received, Preparing, Ready) first, then Delivered orders.
    # Show active orders at the top, then delivered orders.
    active_orders = Order.objects.all().order_by('-id')
    return render(request, 'restaurant/kitchen.html', {
        'orders': active_orders
    })

@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        
        # Handle AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'status': order.status,
                'status_display': order.get_status_display()
            })
            
    return redirect('restaurant:kitchen_dashboard')
