import nmap
import threading
import time
from datetime import datetime
import queue
import requests
import json

my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper




class Scanner:

    def __init__(self, ip):
        self.ip = ip
   
        self.scanner = nmap.PortScanner()
        

    def __repr__(self):
        return f'Scanner:{self.ip}'
    
  
    @storeInQueue
    def portscan_tcp(self):

        self.scanner.scan(self.ip, '1-1024', '-v -sS')
     
        tcp_service_details = {}
        tcp_service_details['Ip'] = self.ip
        tcp_service_details['Ip Status'] = self.scanner[self.ip].state()
        tcp_service_details['Protocol'] = self.scanner[self.ip].all_protocols()
        tcp_service_details['Open Ports'] = self.scanner[self.ip]['tcp']
        return tcp_service_details
        
    @storeInQueue
    def portscan_udp(self):


   
        self.scanner.scan(self.ip, '1-1024', '-v -sU')

        udp_service_details = {}
        udp_service_details['Ip'] = self.ip
        udp_service_details['Ip Status'] = self.scanner[self.ip].state()
        udp_service_details['Protocol'] = self.scanner[self.ip].all_protocols()
        udp_service_details['Open Ports'] = self.scanner[self.ip]['udp']
        return udp_service_details
     

def main_scanner(ip):
    
    # ip_list =['127.0.0.1','8.8.8.8']
    # ip_list = ip_list
    tcp_list = []
    udp_list  = []
    # for  ip in ip_list:
    print("-" * 60)
    print("Please wait, scanning TCP remote host", ip)
    print("-" * 60)

    t_start = datetime.now()
    s = Scanner(ip)
    try:
        # value_tcp = s.portscan_tcp()
        thread_tcp = threading.Thread(target=s.portscan_tcp)
        thread_tcp.start()
        thread_tcp.join()
        value_tcp = my_queue.get()
        print(value_tcp)
            
        t_tcp = datetime.now()
            
        # Calculates the difference of time, to see how long it took to run the script
        total_tcp =  t_tcp - t_start
        print("-" * 60)
        print(f"TCP SCAN FINISH IN {total_tcp} REMOTE HOST",ip)
        print("-" * 60)
    
    except Exception as e:
        raise ValueError("There is problem with TCP Connection.Please Try again. The error is {}".format(e))
        
    t_udp_start = datetime.now() 
    print("-" * 60)
    print(f"UDP SCAN START IN {t_udp_start} REMOTE HOST",ip)
    print("-" * 60)  
    try:
        # value_udp = s.portscan_udp()
        thread_udp = threading.Thread(target=s.portscan_udp)
        thread_udp.start()
        thread_udp.join()
        value_udp = my_queue.get()
        print(value_udp)
        t_udp = datetime.now()
            
        # Calculates the difference of time, to see how long it took to run the script
        total_udp =  t_udp - t_udp_start
        print("-" * 60)
        print(f"UDP SCAN FINISH IN {total_udp} REMOTE HOST",ip)
        print("-" * 60)
    except Exception as e:
        raise ValueError("There is problem with UDP Connection. Please Try again. The error is {}".format(e))
        
       
        # print(value_tcp)
    tcp_list.append(value_tcp) 
    udp_list.append(value_udp)  
    
    t_end = datetime.now()
       
    # Calculates the difference of time, to see how long it took to run the script
    total =  t_end - t_start

    print("-" * 60)
    # Printing the information to screen
    print('Scanning Completed in: {}'.format(total))
    
    print("-" * 60)
    return tcp_list + udp_list
        

def security_headers(url):
    

    url = url
    r = requests.head(url)
    headers_json = json.dumps(dict(r.headers))
    # print(type(response.json()))
    # headers = {}
    # headers['header_info']   =  response.headers
    # headers_data = json.loads(response.headers)
    # print(type(headers_data))
    # print(headers_data)
    # context_header = {
    #     'headers_data': headers_data,
        
    # }
    return headers_json
