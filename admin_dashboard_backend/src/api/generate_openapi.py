"""
Generate OpenAPI specification file from FastAPI app.
Run this script to update the openapi.json file after making changes to the API.
"""
import json
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.api.main import app

if __name__ == "__main__":
    # Get the OpenAPI schema
    openapi_schema = app.openapi()
    
    # Write to file
    output_dir = "interfaces"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "openapi.json")
    
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"OpenAPI specification generated at {output_path}")
