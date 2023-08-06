#PyPing2 main module
#By awesomelewis2007

#If the ip dose not have a http/https site pyping2 will report an error

import requests
import time
def ping(ip):
    """Pings a IP once

    Args:
        ip ([string]): [The address to ping to]

    Returns:
        [pingtimes] [int]: [The ping result in ms]
        [code] [int]: [The ping http code]
    """
    if "https://" in ip:
        pass
    else:
        ip = "https://"+ip
    time_start = time.time()
    request = requests.get(ip)
    time_end = time.time()
    pingtime = time_end - time_start
    code = request.status_code
    return pingtime,code
def multiping(ips):
    """Pings Multiple IP's at one time

    Args:
        ips ([list]): [The list of IP's you want to ping]

    Returns:
        [pingtimes] [list]: [The ping results in ms]
        [code] [list]: [The ping http codes]
    """
    pingtimes = []
    codes = []
    for i in ips:
        if "https://" in i:
            pass
        else:
            i = "https://"+i
        time_start = time.time()
        request = requests.get(i)
        time_end = time.time()
        pingtime = time_end - time_start
        code = request.status_code
        pingtimes.append(pingtime)
        codes.append(code)
    return pingtimes,codes
def demo():
    print("Demo of PyPing2")
    print("Ping time of google.com:"+str(ping("www.google.com")[0]))
    print("Multiping of google.com and github.com:"+str(multiping(["www.google.com","www.github.com"])[0]))