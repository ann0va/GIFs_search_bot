import requests
import constant


def search_gifs(query: object) -> object:

    endpoint = f"https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": 'xNk8MlbJ6qab4vDNq4HDFP6Ew54dsSx3',
        "q": query,
        "limit": 5  
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if response.status_code == 200:
        gifs = data["data"]
        for gif in gifs:
            gif_url = gif["images"]["original"]["url"]
            print(gif_url)
    else:
        print("Error:", data["message"])

if __name__ == "__main__":
    search_term = input("Enter a search word: ")
    search_gifs(search_term)

