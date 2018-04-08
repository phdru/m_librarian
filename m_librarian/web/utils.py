from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB
from os import path, remove
import socket


lock_fname = path.join(
    path.dirname(path.dirname(path.dirname(__file__))),
    'tmp', 'm_librarian.lock')


def get_lock(port):
    try:
        lock_file = open(lock_fname, 'r')
    except IOError:  # no lock file
        pass
    else:
        try:
            flock(lock_file, LOCK_EX | LOCK_NB)
        except IOError:  # locked
            port = int(lock_file.readline())
            lock_file.close()
            return None, port
        else:
            flock(lock_file, LOCK_UN)
            lock_file.close()

    lock_file = open(lock_fname, 'w')
    lock_file.write(str(port))
    lock_file.close()
    lock_file = open(lock_fname, 'r')
    flock(lock_file, LOCK_EX | LOCK_NB)
    return lock_file, None


def close_lock(lock_file):
    flock(lock_file, LOCK_UN)
    lock_file.close()
    lock_file = open(lock_fname, 'w')
    lock_file.write('')
    lock_file.close()
    remove(lock_fname)


def get_open_port():
    # https://stackoverflow.com/a/2838309/7976758
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    # s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
