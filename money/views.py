from django.shortcuts import render
from django.template import loader
import requests
import json

from django.http import HttpResponse


def converter(valute_in, spred):
    valute_out = valute_in * spred
    return valute_out


def index(request):
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    res = requests.get(url)
    cbr_data = json.loads(res.text)
    money_list = [valute for valute in cbr_data['Valute']]
    money_list.append('RUB')

    template = loader.get_template('index.html')
    money_from = 'USD'
    money_to = 'RUB'
    money_from_value = 1

    # if request.method == 'GET':
    #     money_from = 'USD'
    #     money_to = 'RUB'
    #     money_from_value = 1

    if request.method == 'POST':
        money_from = request.POST['money_from']
        money_to = request.POST['money_to']
        money_from_value = float(request.POST['money_from_value'])

    valute_in = cbr_data['Valute'].get(money_from)
    valute_out = cbr_data['Valute'].get(money_to)
    if valute_out is None:
        valute_out = {'Value': 1}

    money_to_value = converter(money_from_value, valute_in.get('Value') / valute_out.get('Value'))

    context = {
        'money_list': money_list,
        'money_from': money_from,
        'money_from_value': money_from_value,
        'money_to': money_to,
        'money_to_value': money_to_value
    }
    return HttpResponse(template.render(context, request))
