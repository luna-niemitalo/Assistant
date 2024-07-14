GetRainProbability_description = {
    "type": "function",
    "function": {
        "name": "get_rain_probability",
        "description": "Get the probability of rain for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
}


def get_rain_probability(location):
    print(f"Getting the probability of rain for {location}")
    return "High"