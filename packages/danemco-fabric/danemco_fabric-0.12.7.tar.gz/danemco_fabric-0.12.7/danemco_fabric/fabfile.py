try:
    from danemco_fabric import *  # noqa
    configure()  # noqa: F405
except ImportError:

    print("Failed to locate danemco-fabric, which is required for most operations")
    print("")
    print("    pip install -e git+git@gitlab.com:virgodev/lib/danemco-fabric.git#egg=danemco_fabric")

    exit(1)
