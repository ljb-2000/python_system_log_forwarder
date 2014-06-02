#!/usr/bin/env python

#Copyright (c) 2014, Dave Stoll dave<dot>stoll<at>gmail<dot>com
#All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from pygtail import Pygtail
from os import path
from time import time
import socket

#for line in Pygtail("some.log"):
#    sys.stdout.write(line)

cycle_rate = 30

# these are all the log files we want to monitor
log_files = ["/var/log/syslog",
			"/var/log/auth.log",
			"/var/log/dmesg",
			"/var/log/kern.log",
			"/var/log/mail.log",
			"/var/log/mail.err",
			"/var/log/ufw.log",
			"/home/kippo/kippo-0.8/log/kippo.log"]

#log_files = ["/var/log/messages",
#                        "/var/log/dmesg",
#                        "/var/log/kern.log",
#                        "/var/log/exim_mainlog",
#                        "/var/log/exim_rejectlog",
#                        "/var/log/secure"]


dst_host = 'dstoll.no-ip.biz'
dst_port = 9999
buffer_size = 1024000

DEBUG=False

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((dst_host, dst_port))
except Exception as e:
	print e
	exit(-1)


while(True):
	start_time = time()
	if DEBUG:
		print 'starting log sweep'

	for file in log_files:
		if DEBUG:
			print 'checking ', file
		if path.exists(file):
			for line in Pygtail(file):
				msg = file.split('/')[-1] + ' - ' + line.rstrip() + '\n'
				try:
					s.send(msg)
				except:
					if DEBUG:
						print 'error, retrying connection.'
					try:
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect((dst_host, dst_port))
						s.send(msg)
					except Exception as e:
						print e
						exit(-1)

	while time() - start_time < cycle_rate:
		pass

s.close()
