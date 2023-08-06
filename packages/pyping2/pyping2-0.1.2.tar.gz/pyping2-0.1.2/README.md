# PyPing2

An easy to use pinging tool
## What is PyPing2
PyPing2 is a ping tool that uses the requests module to see how long it takes to send a request to a webpage

## Usage
PyPing2 has a ping and a multiping
### Standard ping
```python
>>> import pyping2
>>> pyping2.ping("1.1.1.1")
(0.08119845390319824, 200) # 0.081s with a code of 200 
>>> pyping2.ping("https://httpstat.us/400")
(0.21622967720031738, 400) # 0.21s with a code of 400 
```
PyPing2 uses the requests module to get the ping time and http code
### Mulitping
Multiping is where you can ping multiple ip's at once

```python
>>> import pyping2
>>> pyping2.multiping(["www.github.com","https://httpstat.us/300","https://httpstat.us/400","https://httpstat.us/500"])   
([0.25054311752319336, 0.24100875854492188, 0.21611857414245605, 0.22248053550720215], [200, 300, 400, 500])
```
The return is in the order of the list you enter into multiping e.g

```python
#www.github.com,https://httpstat.us/300,https://httpstat.us/400,https://httpstat.us/500
([0.25054311752319336, 0.24100875854492188, 0.21611857414245605, 0.22248053550720215], [200, 300, 400, 500])
```