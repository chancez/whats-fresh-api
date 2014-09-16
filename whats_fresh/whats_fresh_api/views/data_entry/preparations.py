from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.datastructures import MultiValueDictKeyError

from whats_fresh_api.models import *
from whats_fresh_api.forms import *
from whats_fresh_api.functions import *

import json


def preparation_list(request):
    preparations = Preparation.objects.all()
    preparations_list = []

    for preparation in preparations:
        preparation_data = {}
        preparation_data['name'] = preparation.name
        preparation_data['description'] = preparation.description
        preparation_data['link'] = reverse('edit-preparation', kwargs={'id': preparation.id})

        if len(preparation_data['description']) > 100:
            preparation_data['description'] = preparation_data['description'][:100] + "..."

        preparations_list.append(preparation_data)

    return render(request, 'list.html', {
        'parent_url': reverse('home'),
        'parent_text': 'Home',
        'new_url': reverse('new-preparation'),
        'new_text': "New preparation",
        'title': "All preparations",
        'item_classification': "preparation",
        'item_list': preparations_list,
    })


def preparation(request, id=None):
    if request.method == 'POST':
        post_data = request.POST.copy()
        errors = []

        preparation_form = PreparationForm(post_data)
        if preparation_form.is_valid() and not errors:
            preparation = Preparation.objects.create(**preparation_form.cleaned_data)
            preparation.save()
            return HttpResponseRedirect(reverse('entry-list-preparations'))
        else:
            pass
    else:
        preparation_form = PreparationForm()

    title = "Add a Preparation"

    message = "* = Required field"

    post_url = reverse('new-preparation')


    return render(request, 'preparation.html', {
        'parent_url': [
            {'url': reverse('home'), 'name': 'Home'},
            {'url': reverse('entry-list-preparations'), 'name': 'Preparations'}],
        'title': title,
        'message': message,
        'post_url': post_url,
        'errors': [],
        'preparation_form': preparation_form,
    })
