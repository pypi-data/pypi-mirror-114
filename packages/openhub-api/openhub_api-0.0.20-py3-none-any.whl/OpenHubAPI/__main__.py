import socket

from manage.manage import main


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


ip = str(get_my_ip())

main('makemigrations')
main('migrate')
main('runserver', ip + ':8000')
