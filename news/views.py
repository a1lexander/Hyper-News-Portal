from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from datetime import datetime


import json
import random


def main_page(request):
    return redirect('/news/')


json_data = settings.NEWS_JSON_PATH
with open(json_data, 'r') as f:
    data = json.load(f)


class ListView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        if not q:
            context = {'data': data}
            return render(request, 'news/index.html', context=context)
        else:
            search_q = [obj for obj in data if q in obj['title']]
            context = {'data': search_q}
            return render(request, 'news/index.html', context=context)


class CreateView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create_form.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        with open(json_data, "w") as json_file:
            new_data = data
            context = {'created': str(datetime.now())[:19], 'text': text, 'title': title,
                       'link': random.randint(4, 10)}
            new_data.append(context)
            json.dump(new_data, json_file)
        return redirect('/news/')


class DetailView(View):
    def get(self, request, news_id, *args, **kwargs):
        search_data = [obj for obj in data if obj['link'] == news_id][0]
        context = {'data': search_data}
        return render(request, 'news/detail.html', context=context)





