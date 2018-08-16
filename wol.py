#!/usr/bin/env python
'''
Switch on remote computers.

'''
# https://www.vivaolinux.com.br/artigo/Wake-on-LAN-WOL-utilizando-Netcat-Dissecando-o-protocolo
# ^[a-fA-F0-9:]{17}|[a-fA-F0-9-]{17}|[a-fA-F0-9]{12}$
# 00:02:02:34:72:a5
# 00-02-02-34-72-a5
# 0002023472a5


import socket
import struct
import re


def wake_on_lan(macaddress):
    ''' Use macaddresses with any seperators.
    '0F:0F:DF:0F:BF:EF', '0F-0F-DF-0F-BF-EF',
    or without any seperators '0F0FDF0FBFEF' '''

    if not macaddress:
        raise ValueError('Not arguments yet!\nUse wol --help')

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format.')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])

    send_data = bytes()

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = b''.join(
                [send_data, struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        usage='wol 0F:0F:DF:0F:BF:EF')
    parser.add_argument('mac', help=wake_on_lan.__doc__)
    args = parser.parse_args()

    try:
        wake_on_lan(args.mac)
    except Exception as error:
        print(error)
