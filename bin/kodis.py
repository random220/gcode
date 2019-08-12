#!/usr/bin/python

import os,sys,re,tempfile
import time
import socket


os.environ['PATH'] = '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'


def main():
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Bind the socket to the port
  server_address = ('localhost', 8888)
  sock.bind(server_address)

  # Put the socket in server mode
  sock.listen(1)

  # Wait for an incoming connection
  connection, client_address = sock.accept()
  # The connection is actually a different socket on another port (assigned by the kernel).
  # Data is read from the connection with recv() and transmitted with sendall()

  # Receive data 16 bytes at a time
  data = connection.recv(16)
  print('----')
  print(data)

main()
