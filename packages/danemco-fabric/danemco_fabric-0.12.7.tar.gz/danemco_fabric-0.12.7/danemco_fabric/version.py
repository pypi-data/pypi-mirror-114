__version__info__ = (0, 12, 7)


def get_version():
    v = '.'.join([str(i) for i in __version__info__])
    return v


__version__ = get_version()
