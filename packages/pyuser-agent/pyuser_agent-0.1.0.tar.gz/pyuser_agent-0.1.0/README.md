# pyuser_agent
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/THAVASIGTI/pyuser_agent)
[![PyPI](https://img.shields.io/pypi/v/pyuser_agent)](https://pypi.org/project/pyuser_agent)
[![Downloads](https://pepy.tech/badge/pyuser_agent)](https://pepy.tech/project/pyuser_agent)

### A user agent is any software that retrieves and presents Web content for end users or is implemented using Web technologies. User agents include Web browsers, media players, and plug-ins that help in retrieving, rendering and interacting with Web content.

## INSTALL PACKAGE

``` console
pip install pyuser-agent
```

## IMPORT PACKAGE

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyuser_agent
>>> 
```

## USAGE BROWSER NAME
### get browser relative user_agent for `platform` random to generate

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyuser_agent
>>>
# assgin obj 
>>> obj = pyuser_agent.UA()
>>> 
# list of browsers
>>> obj.list
['chrome', 'chromeplus', 'edge', 'firefox', 'internet_explorer', 'mozilla', 'opera', 'safari']
>>> 
# get user agent for browser
>>> obj.chrome
'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2'
>>> 
>>> obj.chromeplus
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/534.10 ChromePlus/1.5.2.0alpha1'
>>> 
>>> obj.edge
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931'
>>> 
>>> obj.firefox
'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.3a3pre) Gecko/20100306 Firefox3.6 (.NET CLR 3.5.30729)'
>>> 
>>> obj.internet_explorer
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; chromeframe/12.0.742.100)'
>>> 
>>> obj.mozilla
'Mozilla/5.0 (X11; U; FreeBSD i386; ja-JP; rv:1.7.2) Gecko/20050330'
>>> 
>>> obj.opera
'Opera/9.80 (S60; SymbOS; Opera Tablet/9174; U; en) Presto/2.7.81 Version/10.5'
>>> 
>>> obj.safari
'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/124 (KHTML, like Gecko)'
>>> 
```
## USAGE RANDOME
### get browser user_agent for `platform`  and `browser` random to generate

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyuser_agent
>>> obj = pyuser_agent.UA()
>>> 
>>> obj.random
'Opera/9.80 (S60; SymbOS; Opera Tablet/9174; U; en) Presto/2.7.81 Version/10.5'
>>> 
>>> obj.random
'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8) Gecko/20060322 Firefox/2.0a1'
>>> 
>>> obj.random
'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.8) Gecko/20071004 Firefox/2.0.0.8 (Debian-2.0.0.8-1)'
>>> 
>>> 
```

## EXCEPTION

### input error key. `random` module execute

``` python
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyuser_agent
>>> obj = pyuser_agent.UA()
>>> 
>>> obj.chr
WARNING:root:not match "chr". return random user agent.
'Mozilla/5.0 (X11; U; Linux i686 (x86_64); nl; rv:1.8.0.6) Gecko/20060728 SUSE/1.5.0.6-1.2 Firefox/1.5.0.6'
>>> 
```