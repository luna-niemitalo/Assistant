import json

from google_search_api.google_search_api import GoogleSearchAPI

GooogleSearch_description = {
    "type": "function",
    "function": {
        "name": "google_search",
        "description": "Search for specified string in google.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_string": {
                    "type": "string",
                    "description": "The string to search for."
                },
            },
            "required": ["url"]
        },
    }
}
def google_search(search_string):
    # Initialize GoogleSearchAPI object
    google_search_api = GoogleSearchAPI()

    # Perform a Google search
    query = search_string
    num_results = 10
    search_results = google_search_api.google_search(query, num_results)

    # Print search results in JSON format
    print(search_results)
    return json.dumps(search_results)


if __name__ == "__main__":
    search_string = "Example site"  # Replace with the actual URL
    extracted_text = google_search(search_string)

    # Print the extracted text
    print(extracted_text)