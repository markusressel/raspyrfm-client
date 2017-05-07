from raspyrfm_client import RaspyRFMClient

rfm_client = RaspyRFMClient()

gateways = rfm_client.search()

for gateway in gateways:
    print(gateway)
