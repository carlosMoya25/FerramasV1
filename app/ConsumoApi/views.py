from django.shortcuts import render

import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from products.models import Product
from django.forms.models import model_to_dict



def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'category': product.category_id,
        'image': product.image.url if product.image else '',
        'excerpt': product.excerpt,
        'detail': product.detail,
        'price': product.price,
        'available': product.available,
    }

@csrf_exempt
@require_http_methods(["GET", "POST"])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_list = [product_to_dict(product) for product in products]
        return JsonResponse(products_list, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product = Product.objects.create(**data)
        return JsonResponse({'id': product.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(product_to_dict(product))
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return JsonResponse(product_to_dict(product))
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)






"""
def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'category': product.category_id,
        'image': product.image.url if product.image else '',
        'excerpt': product.excerpt,
        'detail': product.detail,
        'price': product.price,
        'available': product.available,
    }

def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values())
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product = Product.objects.create(**data)
        return JsonResponse({'id': product.id}, status=201)

def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(model_to_dict(product))
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return JsonResponse(model_to_dict(product))
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)



@csrf_exempt
@require_http_methods(["GET", "POST"])
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values())
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product = Product.objects.create(**data)
        return JsonResponse({'id': product.id}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(model_to_dict(product))
    elif request.method == 'PUT':
        data = json.loads(request.body.decode('utf-8'))
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return JsonResponse(model_to_dict(product))
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)

"""