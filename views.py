from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
import json
import request
from  .validators  import custom_validators,error_response,check_length_of_input,main_validtor_with_results
from  .scanner  import Scanner,main_scanner,security_headers
import requests

# Create your views here.


class ScanView(View):
    def get(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        
        
        # data =  request.body
        validators_check = custom_validators(url=body_data['url'])
        if validators_check.check_url() is False:
            return JsonResponse(error_response(901,"Invalid URL "))
        if check_length_of_input(body_data) is False:
            return JsonResponse(error_response(904,"2 parameters is required "))
        if not isinstance(body_data['ip'], list):
            return JsonResponse(error_response(905,"Ip should be in list"))
        for ip in body_data['ip']:
            if validators_check.check_ip(ip) is False:
                return JsonResponse(error_response(902,"Invalid IP "))
        
        data_service_list =  main_validtor_with_results(body_data)
        headers_info = security_headers(body_data['url'])
        # response = requests.head(body_data['url'])
        # # print(validators_check.check_url())
        # data_service_list = []
        # for ip in body_data['ip']:
        #     if validators_check.check_ip(ip) is False:
        #         return JsonResponse(error_response(902,"Invalid IP "))
        #     data_from_scanning = main_scanner(ip)
        #     data_service_list.append(data_from_scanning)
        # print(str(security_headers(body_data['url']))
        
        context = {
                    'input_details':body_data,
                    'service_details': data_service_list,
                    'security_info': headers_info
                   }
        # print(security_headers(body_data['url']))
        # context['header'] = {
            
            
        # }
        # context = {}
        # context['header'] = response.headers
        return JsonResponse(context)

    def post(self, request, *args, **kwargs):
        data =  request.body
        print(data)
        context = {
            'object_list': data,
            
        }
        return JsonResponse(context)

