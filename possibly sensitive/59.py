		destroyPinger = dummy
		if pinger is None:
			pinger = ping.Pinger(self.host, bytes(self.conf.PAYLOAD))
			destroyPinger = lambda x: x.sock.close()


		rtt, lost = [], 0

		results = pool.map_async(pinger.ping,
		                              range(self.conf.NUMPINGS),
		                              error_callback=utils.error)
		pkts = results.get(2)

		for pkt in pkts:
			if pkt != None and pkt > 0:
				rtt.append(pkt*1000)
			else:
				lost += 1

		try:
			avg = sum(rtt) / len(rtt)
			std = 0.
			for item in rtt:
				std += (avg - item)**2
			std /= len(rtt) - 1
			std = math.sqrt(std)
		except ZeroDivisionError:
			std = 0.
		finally:
			destroyPinger(pinger)

		if rtt:
			self.result[0] = utils.PingResult(min(rtt), avg, max(rtt), std, lost/self.conf.NUMPINGS *100.0)
		else:
			self.result[0] = type(self).result[0]


	def __str__(self) -> str:

		ret = []
		if self.host[0] == self.hostname:
			ret.append(self.hostname)
		else:
			ret.append("%s (%s)" % (self.hostname, self.host[0]))

		pings, trace, scans = self.result

		if pings:
			ret.append(str(pings))
		if trace and trace != self.trace:

			ret.append(utils.traceToStr(trace))
		if scans:
			ret.append(str(scans))

		return "\n".join(ret)

	def __repr__(self) -> repr:
rns a JSON output result
		
		ret = [r'{"addr":"%s"' % self.host[0]]
		ret.append(r'"name":"%s"' % self.hostname)

		if not self.conf.NOPING:
			ret.append(r'"ping":%s' % repr(self.result[0]))

		if self.conf.TRACE and self.trace != self.result[1]:
			self.trace = self.result[1]

			ret.append(r'"trace":%s' % utils.traceRepr(self.result[1]))

		if self.conf.PORTSCAN:
			ret.append(r'"scan":%s' % repr(self.result[2]))

		return ','.join(ret) + '}'


	def recv(self):

		return self.pipe[0].recv()
