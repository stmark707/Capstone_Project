import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


"""Add a user to the virtual users table.

        AuthorizerError exceptions raised on error conditions such as
        invalid permissions, missing home directory or duplicate usernames.

        Optional perm argument is a string referencing the user's
        permissions explained below:

        Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
         - "r" = retrieve file from the server (RETR command)

        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
         - "M" = change file mode (SITE CHMOD command)
         - "T" = update file last modified time (MFMT command)

        Optional msg_login and msg_quit arguments can be specified to
        provide customized response strings when user log-in and quit.
"""


bar_dir = ('ftp_files')
authorizer = DummyAuthorizer()

authorizer.add_user('barcode_scanner', 'csc480', bar_dir, perm= 'elradfmwMT')

handler = FTPHandler
handler.authorizer = authorizer

handler.passive_ports = range(60000, 65535)

handler.banner = 'Barcode has successfully connected to ftp server'

ip_address = ('192.168.1.24', 21)
server = FTPServer(ip_address, handler)

server.max_cons = 2
server.max_cons_per_ip = 5

try:
    server.serve_forever()
    print('opened server')
except KeyboardInterrupt:
    server.close_all()
    print('Closing server')