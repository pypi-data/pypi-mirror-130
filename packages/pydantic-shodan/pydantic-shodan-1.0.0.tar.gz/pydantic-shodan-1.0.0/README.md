# pydantic-shodan
Python 3 library containing Pydantic models for parsing and validating [Shodan banners](https://datapedia.shodan.io/).

## About
It is based on the [JSON schema](https://datapedia.shodan.io/banner.schema.json) provided by Shodan and extended with fields such as `ethereum_p2p` that are not documented in the schema but occasionally present in the banner. The library was tested with on approximately 300k banners.

## Installation
```bash
pip install pydantic-shodan
```

## Example
```python
import json
from pydantic_shodan import Banner

BANNER_JSON = """
{
    "_shodan": {
        "id": "7383056c-d513-4b43-8734-b82d897888e6",
        "options": {},
        "ptr": true,
        "module": "dns-udp",
        "crawler": "9d8ac08f91f51fa9017965712c8fdabb4211dee4"
    },
    "hash": -553166942,
    "os": null,
    "opts": {
        "raw": "34ef818200010000000000000776657273696f6e0462696e640000100003"
    },
    "ip": 134744072,
    "isp": "Google",
    "port": 53,
    "hostnames": [
        "dns.google"
    ],
    "location": {
        "city": null,
        "region_code": null,
        "area_code": null,
        "longitude": -97.822,
        "country_code3": null,
        "country_name": "United States",
        "postal_code": null,
        "dma_code": null,
        "country_code": "US",
        "latitude": 37.751
    },
    "dns": {
        "resolver_hostname": null,
        "recursive": true,
        "resolver_id": null,
        "software": null
    },
    "timestamp": "2021-01-28T07:21:33.444507",
    "domains": [
        "dns.google"
    ],
    "org": "Google",
    "data": "Recursion: enabled",
    "asn": "AS15169",
    "transport": "udp",
    "ip_str": "8.8.8.8"
}
"""

banner = Banner.parse_obj(json.loads(BANNER_JSON))
```