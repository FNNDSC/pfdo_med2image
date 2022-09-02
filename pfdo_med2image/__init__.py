from importlib.metadata import Distribution

__pkg = Distribution.from_name(__package__)
__version__ = __pkg.version

try:
    from .pfdo_med2image    import pfdo_med2image
except:
    from pfdo_med2image     import pfdo_med2image
