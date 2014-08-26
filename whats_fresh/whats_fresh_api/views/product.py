from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
import json


def product_list(request):
    """
    */products/*

    Returns a list of all products in the database. In the future this function
    will support the ?limit=<int> parameter to limit the number of products
    returned.
    """
    data = {}
    product_list = Product.objects.all()

    if len(product_list) == 0:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'No products were found',
            'error_name': 'Products not found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json",
            status=404
        )

    data['products'] = []
    try:
        for product in product_list:
            data['products'].append(model_to_dict(product, fields=[], exclude=[]))
            del data['products'][-1]['preparations']
            del data['products'][-1]['image_id']

            data['products'][-1]['image'] = product.image_id.image.url
            data['products'][-1]['created'] = str(product.created)
            data['products'][-1]['modified'] = str(product.modified)
            data['products'][-1]['id'] = product.id

        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': str(e),
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def product_details(request, id=None):
    """
    */products/<id>*

    Returns the product data for product <id>.
    """
    data = {}

    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Product id %s was not found' % id,
            'error_name': 'Product Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=404
        )

    try:
        data = model_to_dict(product, fields=[], exclude=[])
        del data['preparations']
        del data['image_id']

        data['image'] = product.image_id.image.url
        data['created'] = str(product.created)
        data['updated'] = str(product.modified)
        data['id'] = product.id

        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except:
        error_text = 'An unknown error occurred processing product %s' % id
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': error_text,
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )

def product_vendor(request, id=None):
    data = {}

    try:
        product_list = Product.objects.filter(productpreparation__vendorproduct__vendor__id__exact=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Vendor id %s not found' % id,
            'error_name': 'Vendor Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json",
            status=404
        )
 
    data['products'] = []
    try:
        for product in product_list:
            data['products'].append(model_to_dict(product, fields=[], exclude=[]))
            del data['products'][-1]['preparations']
            del data['products'][-1]['image_id']

            data['products'][-1]['story_id'] = product.story_id.id
            data['products'][-1]['image'] = product.image_id.image.url
            data['products'][-1]['created'] = str(product.created)
            data['products'][-1]['modified'] = str(product.modified)
            data['products'][-1]['id'] = product.id
           
        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        error_text = 'An unknown error occurred processing product %s' % id
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': error_text,
            'error_name': str(e)
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
