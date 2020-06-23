
from validator_collection import validators, checkers
import re 
from django.http import JsonResponse
from  .scanner  import Scanner,main_scanner,security_headers

class custom_validators:

    def __init__(self, url,*args,**kwargs):

        self.url = url

        # self.ip = [**kwargs]

    def __repr__(self):
        return f'url:{self.url} ip:{self.ip}'

    def check_ip(self,ip):
        # Make a regular expression 
        # for validating an Ip-address 
        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
            # pass the regular expression 
        # and the string in search() method 
        
        if re.search(regex, ip): 
            return True
        else: 
            return False





    def check_url(self):

        return checkers.is_url(self.url)

def check_length_of_input(data):
    if len(data) != 2:
        return False

def error_response(error_code,error_type):
    error =  {
		"error_code":error_code,
		"description":error_type
	}
    
    return error
def main_validtor_with_results(body_data):
    
        # validators_check = custom_validators(url=body_data['url'])
        # if validators_check.check_url() is False:
        #     return JsonResponse(error_response(901,"Invalid URL "))
        # if check_length_of_input(body_data) is False:
        #     return JsonResponse(error_response(904,"2 parameters is required "))
        # if not isinstance(body_data['ip'], list):
        #     return JsonResponse(error_response(905,"Ip should be in list"))
            
        # print(validators_check.check_url())
        data_service_list = []
        for ip in body_data['ip']:
            # if validators_check.check_ip(ip) is False:
            #     return JsonResponse(error_response(902,"Invalid IP "))
            data_from_scanning = main_scanner(ip)
            data_service_list.append(data_from_scanning)
            
        return data_service_list

