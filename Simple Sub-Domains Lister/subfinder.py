import subprocess as sp
import os
import re
from socket import gethostbyname


def get_subdomains(website):
    core = website.split('.')[1]
    rge =f'([A-Za-z0-9\.\-/]+://)?([A-Za-z0-9\.\-]+\.{core}\.\w+)'
    HTMLPage = sp.run(f"wget {website}", capture_output= True, text = True, cwd =os.getcwd(), shell = True)

    subdomains = []
    with open('index.html','r') as indexFile:
        content = indexFile.read()
        data = re.findall(rge, content)
    
    for subdomain in data:
        subdomain = "".join(subdomain)
        if subdomain not in subdomains:
            subdomains.append(subdomain)
    return subdomains


def checksub(subs):
    subIPs = []
    for sub in subs:
        hostname = sub.split("//")
        if len(hostname) == 1:
            hostname = hostname[0]
        else:
            hostname = hostname[1]
        try:
            hostIP = gethostbyname(hostname)
            if hostIP not in subIPs:
                status = sp.run(f'ping -c 1 {hostIP}', text = True, shell= True,cwd=os.getcwd(), capture_output= True)
                status = status.returncode
                if status == 0:
                    print(f"{sub} ==> {gethostbyname(hostname)} ==> host is active")
                else:
                    print(f"{sub} ==> {gethostbyname(hostname)} ==> host is idle")
                subIPs.append(hostIP)
        
        except:
            print(f"{hostname} ==> host is not found")
            
            
            
subs = get_subdomains("www.cisco.com")  
checksub(subs)      
sp.run("rm -f index.html",shell = True,cwd = os.getcwd())
        
   
   
   
    