import requests

summarize_description = {
    "type": "function",
    "function": {
        "name": "text_summarize", #Note the name in the description needs to match the function name, and be unique
        "description": "Summarize a given text.",
        "parameters": { # The parameters need to match the parameters of the called function
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text that needs to be summarized."
                },
            },
            "required": ["text"]
        },
    }
}

def text_summarize(text):
    url = 'https://api.summarizationtool.com/summarize'
    response = requests.post(url, json={'text': text})
    return response.json()

if __name__ == "__main__":
    example_text = "This is a long text that needs to be summarized. It talks about various important topics that should be condensed for quicker reading."
    summary = text_summarize(example_text)
    print(summary)