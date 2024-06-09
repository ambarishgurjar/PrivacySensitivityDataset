				time.sleep(5)
				if not collectors or not any(c.is_alive() for c in collectors):
					return 1
			except ContinueException:
				pass

	except KeyboardInterrupt:
		for c in collectors:
			c.pipe[0].send(True)
		for c in collectors:
			c.join()
	except Exception as e:
		utils.error(e)
		return 1
	print() # Flush the buffer
	return 0

def readConf():

	global collectors, confFile, config
if file pointed to

	if confFile:
		try:
			file = open(confFile)
		except OSError as e:
			utils.error(FileNotFoundError("Couldn't read input file '%s'"%e), fatal=True)
		hosts = file.readlines()
		file.close()


	else:
		hosts = sys.stdin.readlines()

	collectors = []


	for i,host in enumerate(hosts):

		if not host.strip():
			continue

		args = host.split()
		host = args.pop(0)
		addrinfo = utils.getaddr(host)
		if not addrinfo:
			utils.error(Exception("Unable to resolve host ( %s )" % host))
			sys.stderr.flush()
			continue

		conf = {"HOSTS": {host: addrinfo}}
		try:
			for arg, value in [a.upper().split('=') for a in args]:
				conf[arg] = config[arg](value)
		except ValueError as e:
			utils.error(IOError("Error parsing value for %s: %s" % (arg,e)), True)
		except KeyError as e:
			utils.error(IOError("Error in config file - unknown option '%s'" % arg), True)

		collectors.append(Collector(host, i+1, Config(**conf)))

	if not collectors:
		utils.error(Exception("No hosts could be parsed!"), fatal=True)

class ContinueException(Exception):

	pass
