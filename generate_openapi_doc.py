import requests
import json

# Fetch the OpenAPI schema
url = 'http://127.0.0.1:8000/openapi.json'
response = requests.get(url)

# Save the JSON to a file
with open('openapi_schema.json', 'w') as json_file:
    json.dump(response.json(), json_file, indent=4)  # Use json.dump for proper formatting


def convert_to_markdown(openapi_schema):
    # Check if 'info' exists and has required fields
    info = openapi_schema.get('info', {})
    title = info.get('title', 'API Documentation')
    description = info.get('description', 'No description provided.')

    markdown = f"# {title}\n\n"
    markdown += f"## Description\n{description}\n\n"
    markdown += "## Endpoints\n\n"

    # Iterate through the paths and methods
    for path, methods in openapi_schema.get('paths', {}).items():
        for method, details in methods.items():
            summary = details.get('summary', 'No summary provided.')
            # Add the method description if available
            method_description = details.get('description', 'No description available.')

            markdown += f"### {method.upper()} {path}\n"
            markdown += f"- Summary: {summary}\n"
            markdown += f"- Description: {method_description}\n\n"

    return markdown


# Load the JSON schema and convert to Markdown
openapi_schema = response.json()
markdown_content = convert_to_markdown(openapi_schema)

# Save the Markdown content
with open('api_documentation.md', 'w') as md_file:
    md_file.write(markdown_content)

print("API documentation has been generated successfully.")