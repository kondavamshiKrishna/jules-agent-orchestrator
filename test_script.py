import urllib.request
import json
def search_pypi(query):
    url = f"https://pypi.org/pypi/{query}/json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"PyPI: Found {query}: {data['info']['project_url']}")
            return True
    except Exception as e:
        print(f"PyPI: Error fetching {query}: {e}")
        return False

search_pypi("pnsea")
search_pypi("nselib")
search_pypi("jugaad-data")
search_pypi("yfinance")
