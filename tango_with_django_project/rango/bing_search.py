import json
import urllib

def read_bing_key():
    bing_api_key = None

    try:
        with open('bing.key', 'r') as f:
            bing_api_key = f.readline()

    except:
        raise IOError('bing.key file not found')

    return bing_api_key

def run_query(search_terms):
	
    bing_api_key = read_bing_key()
    if not bing_api_key:
        raise KeyError('Bing Key Not Found')

    # Specify the base url and the service (Bing Search API 2.0)
    root_url = 'https://api.cognitive.microsoft.com/bing/v7.0/search'

    import requests
    headers = {"Ocp-Apim-Subscription-Key" : bing_api_key}
    params  = {"q": search_terms, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(root_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    from bs4 import BeautifulSoup
    results = []
    print(search_results['webPages'])
    for result in search_results['webPages']['value']:
        results.append({
            'title': BeautifulSoup(result['name'], 'lxml').text,
            'link': BeautifulSoup(result['url'],'lxml').text,
            'summary': BeautifulSoup(result['snippet'],'lxml').text})


    # Return the list of results to the calling function.
    return results


def main():
	print("Enter a query ")
	query = input()
	results = run_query(query)
	for result in results:
		print(result['title'])
		print('-'*len(result['title']))
		print(result['summary'])
		print(result['link'])

if __name__ =='__main__':
    main()