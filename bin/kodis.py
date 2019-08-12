#!/usr/bin/python

import os,sys,re,tempfile
import time
import socket


os.environ['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'


def main():
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
  print('--11')
  while True:
    print('--22')
    print(text_received)
    # Receive data 16 bytes of data
    data = connection.recv(16)
    if data:
      print('--33')
      text_received = text_received+data
    else:
      print('--44')
      break
  print('--55')
  print(text_received)

  now = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())
  # Mon, 12 Aug 2019 06:24:40 UTC
  real_message = '<html><body><h1>It works!</h1></body></html>'
  nbytes = str(len(real_message)-5)
  
  
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

  print('----')
  connection.sendall(text_tosend)
  connection.close()

main()




  
  
