python_system_log_forwarder
===========================

Simple python script that will monitor any number of system log files and 
forward the messages to a remote host using tcp.

Prerequisites:

	*  You will need pygtail.  You can download a copy from the repository here:
		https://github.com/bgreenlee/pygtail

This is a quick and dirty remote log forwarder.  I was working with some data 
analytics software and wanted to forward text log messages to that product.
On the receiver end, just set up a TCP listener.  Netcat will even work.

Before running, edit the list named log_files.  That should be a list of
string file names.  This script will not work on windows the way it is written
it should be re-written to use os.path to separate the filename components for 
platform interoperability.

Finally, set the destination IP address and port by changing dst_host and dst_port 
respectively.

If DEBUG is set to true, caveman debugging will start printing to STDOUT.

This was a quick and dirty solution to a problem.  If you have improvements or find
a bug, feel free to fork and submit a merge request.  Thanks and enqoy.  If you have
issues, feel free to contact me at dave<dot>stoll<at>gmail<dot>com.
