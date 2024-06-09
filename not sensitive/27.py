from subprocess import PIPE, run
import os, csv, re, sys, json, subprocess, socks, httplib2
import urllib.request as request


def onionStatus(url):
	try:
	        proxy = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_SOCKS5, proxy_host='localhost', proxy_port=9050)
	        http = httplib2.Http(proxy_info=proxy, timeout=30)
	        resp = http.request(url, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})[0]
	        return resp.status
	except:
		return 404


def onionHTML(url):
	try:
		proxy = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_SOCKS5, proxy_host='localhost', proxy_port=9050)
		http = httplib2.Http(proxy_info=proxy, timeout=30)
		content = http.request(url, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})[1]
		html = str(content,'utf-8').replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('\"','')
		return html
	except:
		return "None"

def onionExtractor(html,inputUrl):
        results,onions = [],[]
        regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.onion\/?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
        inputRegex = r"\"" + inputUrl + "?[-a-zA-Z0-9@:%._\/+~#=]{1,256}"
        inputMatches = re.finditer(inputRegex, html, re.MULTILINE)
        matches = re.finditer(regex, html, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
                url = (match.group())
                results.append(url)
                onions = list(set(results))
        for matchNum, match in enumerate(inputMatches,start=1):
                url = (match.group())
                results.append(url)
                onions = list(set(results))
        return onions