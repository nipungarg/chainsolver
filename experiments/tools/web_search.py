import requests


def web_search(query):

    try:

        url = "https://api.duckduckgo.com/"

        params = {
            "q": query,
            "format": "json",
            "no_redirect": 1,
            "skip_disambig": 1
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("Abstract"):
            return data["Abstract"]

        if data.get("RelatedTopics"):
            topics = data["RelatedTopics"]

            if len(topics) > 0 and "Text" in topics[0]:
                return topics[0]["Text"]

        return "No useful search results found."

    except Exception as e:
        return f"Search error: {str(e)}"