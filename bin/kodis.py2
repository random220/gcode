#!/usr/bin/python

import os,sys,re,tempfile
import time
import socket


os.environ['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'



def main():
    # https://realpython.com/python-sockets/#echo-client-and-server
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 8888       # Port to listen on (non-privileged ports are > 1023)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
	    print('Connected by', addr)
	    while True:
		data = conn.recv(1024)
		if not data:
		    break
		#conn.sendall(respond(data))
		conn.sendall(data)

def respond(data):
    now = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())
    # Mon, 12 Aug 2019 06:24:40 UTC
    real_message = '<html><body><h1>It works!</h1></body></html>'
    nbytes = str(len(real_message)+1)
    
    text_tosend = '''\
HTTP/1.1 200 OK
Date: {now}
Server: Apache/2.2.14 (Win32)
Last-Modified: {now}
ETag: "10000000565a5-2c-3e94b66c2e680"
Accept-Ranges: bytes
Content-Length: {nbytes}
Connection: close
Content-Type: text/html
X-Pad: avoid browser bug

{message}
'''.format(now=now, nbytes=nbytes, message=real_message)
  
    return text_tosend

def main0():
  # https://pymotw.com/2/socket/tcp.html

  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Bind the socket to the port
  # server_address = ('localhost', 8888)      # only to localhost
  # server_address = ('192.168.10.157', 8888) # only to a specific address
  server_address = ('0.0.0.0', 8888)        # all ip addresses
  sock.bind(server_address)

  # Put the socket in server mode
  sock.listen(1)

  # Wait for an incoming connection
  connection, client_address = sock.accept()
  # The connection is actually a different socket on another port (assigned by the kernel).
  # Data is read from the connection with recv() and transmitted with sendall()

  text_received = ''
  recv_size = 100
  try:
    while True:
      # Receive data 16 bytes of data
      data = connection.recv(recv_size)
      text_received = text_received+data
      if len(data) < recv_size:
        break
    with open('a.txt', 'wt') as f:
      f.write(text_received)
  
    now = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())
    # Mon, 12 Aug 2019 06:24:40 UTC
    real_message = '<html><body><h1>It works!</h1></body></html>'
    nbytes = str(len(real_message)+1)
    
    
    text_tosend = '''\
HTTP/1.1 200 OK
Date: {now}
Server: Apache/2.2.14 (Win32)
Last-Modified: {now}
ETag: "10000000565a5-2c-3e94b66c2e680"
Accept-Ranges: bytes
Content-Length: {nbytes}
Connection: close
Content-Type: text/html
X-Pad: avoid browser bug

{message}
'''.format(now=now, nbytes=nbytes, message=real_message)
  
    connection.sendall(text_tosend)

  except:
    print('--here')
  finally:
    print('--there')
    connection.close()
    sock.shutdown()
    sock.close()

main()




  
  
