"""
Was originally this monstrosity below

[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
 if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
 s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

"""

import socket
from re import compile


def local_ip_address(incorrect_address=compile(r'^127\..*$'), public_dst='8.8.8.8'):
    """Get the local IP address of this host.

    :param incorrect_address: compiled regular expression matching unacceptable addresses.
                              For example, the default filters out loopback addresses like 127.0.0.1
                              You might want to use ``re.compile(r'^(127|172)\..*$')`` to match either
                              127.0.* or 172.*, which will be produced by Docker networks.
    :param public_dst: if the local IP address cannot be determined without the network,
                       then try connecting to the given public_dst ip address.
                       This host's local IP address is discovered from the route.
    """
    # list of ip addresses of this host
    ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
    # might contain loopback address 127.0.0.1
    ip_list = list(filter(lambda ip: not incorrect_address.match(ip), ip_list))
    if len(ip_list) > 0:
        return ip_list[0]
    # try to find IP address from a route
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((public_dst, 53))
        return s.getsockname()[0]

if __name__ == '__main__':
    print(local_ip_address())
