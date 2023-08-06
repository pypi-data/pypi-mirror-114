import psutil


def print_mem():
    mem = psutil.virtual_memory()
    used = mem.used / 1e9
    total = mem.total / 1e9
    print(f'{used:.2f} GB / {total:.2f} GB ({(mem.used / mem.total) * 100:.2f}%)')


if __name__ == '__main__':
    print_mem()
