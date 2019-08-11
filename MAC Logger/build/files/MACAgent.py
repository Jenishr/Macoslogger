#### Syslog Agent for MAC OS X ######
import re
import os
import subprocess
import datetime
import argparse
import logging
import logging.handlers
import socket
import ConfigParser

agent_name=socket.gethostname()
filedir= "/Users/SysAdmin/Integrator"
cfgfile=os.path.join(filedir, 'Sysconfig.ini')
Config =ConfigParser.RawConfigParser()
Config.read(cfgfile)
address=Config.get("SyslogManager", "Sysconfig IP Address")
port=Config.getint("SyslogManager", "Port")
gdata =Config.get("SyslogManager", "lastsend")
Protocol =Config.get("SyslogManager", "Protocol")
if Protocol == "UDP":
	sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
	sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result= sock.connect_ex((address, port))
if result == 0:
	auditfile=[]
	now=datetime.datetime.now()
	nowd=now.strftime("%Y%m%d%H%M%S")
	if gdata:
		enddate=gdata
	else:
		enddate =nowd
	adata=[]
	datas=[]
	rx="(?<=0x\d{8}\:)\w+\:.*"
	data="0x0000020:fm:file read"
	arr = os.listdir('/var/audit/')
	for afile in arr:
		if re.match(enddate[:8], afile):
			auditfile.append(afile)
	if not auditfile:
		auditfile.append("current")
	mdata= re.search(rx, data)
	syslogger = logging.getLogger('ETAgent_MAC')
	syslogger.setLevel(logging.DEBUG)
	if Protocol == "UDP":
		handler = logging.handlers.SysLogHandler(address=(address, port),facility=19)
	else:
		handler = logging.handlers.SysLogHandler(address=(address, port),facility=19,socktype=socket.SOCK_STREAM)
	formatmsg = '%(agent)s %(name)s:  Hostname:%(agent)s  %(message)s'
	formatter=logging.Formatter(formatmsg)
	handler.setFormatter(formatter)
	syslogger.addHandler(handler)
	d= {'agent':agent_name}
	for ffile in auditfile:
		command = "sudo /usr/sbin/auditreduce -a "+enddate+" /var/audit/"+ffile+"| /usr/sbin/praudit -l"
		nowd=now.strftime("%Y%m%d%H%M%S")
		Config.set("SyslogManager", "lastsend", nowd)
		with open(cfgfile, "w") as ld:
			Config.write(ld)
			ld.close()
		m=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		for lline in m.stdout:
			sm=lline.rstrip()
			syslogger.log(20, sm, extra=d)
else:
	if gdata == "":
		now=datetime.datetime.now()
		nowd=now.strftime("%Y%m%d%H%M%S")
		Config.set("SyslogManager", "lastsend", nowd)
		with open(cfgfile, "w") as ld:
			Config.write(ld)
			ld.close()
	exit()
