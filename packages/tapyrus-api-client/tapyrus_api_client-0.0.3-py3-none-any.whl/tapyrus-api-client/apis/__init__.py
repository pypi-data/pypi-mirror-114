
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.address_api import AddressApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from tapyrus-api-client.api.address_api import AddressApi
from tapyrus-api-client.api.payment_api import PaymentApi
from tapyrus-api-client.api.timestamp_api import TimestampApi
from tapyrus-api-client.api.token_api import TokenApi
from tapyrus-api-client.api.user_api import UserApi
