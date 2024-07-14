GetCurrentTemperature_description = {
    "type": "function",
    "function": {
        "name": "get_current_temperature",
        "description": "Get the current temperature for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["Celsius", "Fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the user's location."
                }
            },
            "required": ["location", "unit"]
        }
    }
}


def get_current_temperature(location, unit):
    # Call the weather API to get the current temperature
    print(f"Getting the current temperature for {location} in {unit}")
    return "57"
