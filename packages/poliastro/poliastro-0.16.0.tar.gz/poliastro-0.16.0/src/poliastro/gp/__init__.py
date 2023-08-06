"""
General Perturbations data.

>>> from poliastro import gp
>>> with open("...") as fh:
>>>     iss_tle = gp.load(fh)
>>> iss_tle = gp.loads(httpx.get("...").text)

Notes
-----

- Do *not* see ccsds_ndm, it's GPL!
- Depending on beyond is not that straightforward
  because we don't like unicode attributes,
  we might have to copy-paste the code.
  (And the tests?)
- Sadly jplephem will not suffice.
- Probably we should create our own separate library
  for anybody to use.

"""

import attr


# This assumes that a TLE and an OMM
# can have the same class
# because they represent the same thing!
# Although I'm sure that OMM carries some extra data
# that we should take into account here
@attr.frozen
class GP:
    satnum: int
    classification: str
    epoch: str  # Alternatively, dt.datetime

    ndot: float
    ndotdot: float
    bstar: float

    inc: float
    raan: float
    ecc: float
    argp: float
    M: float
    n: float
    revnum: int


# Evil?
TLE = GP
OMM = GP

# Notice that
# Orbit = OPM
# Ephem = OEM
# ... = OMM
# Naming this is important!
# And probably "GP" is not a good name,
# but I'll let Dr. Kelso convince me

# Also, notice that currently Orbit objects
# don't have all the required information
# to be exported to an OPM

# The OPM has some preferred units!
# We could state those more clearly

# Do I need a separate State?
# Or could I reuse it for the MeanOrbit?

# Also, the I/O framework below is quite ambitious,
# and should definitely be deferred for some other time

# Do we _need_ the MeanOrbit for the tutorial?
# Probably not: it's enough to compute the Ephem for now
# (although we will need some basic I/O for that)


def load(fh, *, format=None):
    return loads(fh.read(), format=format)


def loads(s, *, format=None):
    format = format or _infer_format(s)
    if not format:
        raise ValueError("format not given and could not be inferred from input data")

    ...


def _infer_format(s):
    ...


def _loads_tle(s):
    lines = s.splitlines()
    if len(lines) == 2:
        line1, line2 = lines
    elif len(lines) == 3:
        line0, line1, line2 = lines
    else:
        raise ValueError("Invalid TLE")

    ...


def _loads_omm_xml(s):
    ...

