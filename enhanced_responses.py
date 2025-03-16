import requests
import json
import re


def clean_response(response):
    """Cleans up the response by removing unwanted characters and formatting."""
    return re.sub(r"\s+", " ", response.strip())


def fetch_from_duckduckgo(input_words):
    """Fetches responses from DuckDuckGo API."""
    try:
        ddg_response = requests.get(
            f"https://api.duckduckgo.com/?q={'+'.join(input_words)}&format=json&no_html=1",
            timeout=5
        )
        if ddg_response.status_code == 200:
            data = ddg_response.json()
            if data.get("AbstractText"):
                # Print the processing query sentence
                print(f"Processing Query [DuckDuckGo]: {clean_response(data['AbstractText'])}")
                return data["AbstractText"]
    except Exception as e:
        print(f"Error fetching from DuckDuckGo: {e}")
    return None


def fetch_from_dictionary_api(word):
    """Fetches word definitions from Dictionary API."""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                meaning = data[0]['meanings'][0]['definitions'][0]['definition']
                # Print the processing query sentence
                print(f"Processing Query [Dictionary API]: Definition of {word}: {meaning}")
                return f"Definition of {word}: {meaning}"
    except Exception as e:
        print(f"Error fetching from Dictionary API for {word}: {e}")
    return None


def fetch_from_additional_apis():
    """Fetches random content from additional APIs."""
    apis = [
        ("https://api.quotable.io/random", lambda data: f"{data['content']} — {data['author']}"),
        ("https://v2.jokeapi.dev/joke/Any?type=single", lambda data: data['joke']),
        ("https://api.adviceslip.com/advice", lambda data: data['slip']['advice']),
        ("http://numbersapi.com/random/trivia?json", lambda data: data['text']),
        ("https://poetrydb.org/random", lambda data: f"Poem: {data[0]['title']} by {data[0]['author']}\n" + "\n".join(data[0]['lines'])),
        ("https://opentdb.com/api.php?amount=1", lambda data: f"Trivia: {data['results'][0]['question']} Answer: {data['results'][0]['correct_answer']}"),
        ("http://www.boredapi.com/api/activity/", lambda data: f"Activity: {data['activity']}"),
        ("https://uselessfacts.jsph.pl/random.json?language=en", lambda data: data['text']),
        ("https://yesno.wtf/api", lambda data: f"Answer: {data['answer']}")
    ]
    for url, parser in apis:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = parser(data)
                if result:
                    # Print the processing query sentence
                    print(f"Processing Query [Additional API]: {result}")
                    return result
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return None


def enhanced_response_generation(input_words):
    """Generates enhanced responses based on input words."""
    # Try DuckDuckGo API first
    primary_response = fetch_from_duckduckgo(input_words)
    if primary_response:
        return primary_response

    # Try Dictionary API for each word
    for word in input_words:
        definition = fetch_from_dictionary_api(word)
        if definition:
            return definition

    # Try additional APIs for random content
    fallback_response = fetch_from_additional_apis()
    if fallback_response:
        return fallback_response

    # Default response if all APIs fail
    return "I'm sorry, I couldn't find any relevant information. Please try rephrasing your query."


# Example Usage
if __name__ == "__main__":
    words = ["example", "test"]
    response = enhanced_response_generation(words)
    print(f"\nFinal Response: {response}")
