import zmq

class ZMQHelper:
    def __init__(self):
        self.context = zmq.Context()
    def newSocket(self, stype, ip, ports, udp = False):
        """Create a Socket connecting to given ports, pass a list of zero ports if you want to create a socket only.

        Parameters
        ----------
        stype : int
            The socket type, which can be any of the 0MQ socket types:
            REQ/REP, PUB/SUB, PULL/PUSH.
        ip : str
            ip address which the socket will connect to
        ports : list
            list of ports to connect to
        udp : bool
            False by default meaning TCP connection protocol, if true the UDP will be used 
        """
        return self._socket(stype, ip, ports, "connect", udp)

    def newSocketMultiIps(self, stype, ips, port, udp = False):
        protocol = "udp" if udp else "tcp"
        s = self.context.socket(stype)
        for ip in ips:
            s.connect(f"{protocol}://{ip}:{port}")
        return s
    def newServerSocket(self, stype, ip, port, udp = False):
        # TODO: don't take the ip parameter here, or send it and as the user wants send
        return self._socket(stype, "*", [port,], "bind", udp)
        # return self._socket(stype, ip, [port,], "bind", udp)

    def _socket(self, stype, ip, ports, function, udp = False):
        protocol = "udp" if udp else "tcp"
        s = self.context.socket(stype)
        for port in ports:
            getattr(s, function)(f"{protocol}://{ip}:{port}")
        return s
zhelper = ZMQHelper()