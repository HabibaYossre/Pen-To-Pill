import requests
import sys
import json
from pathlib import Path

def test_prescription_api(image_path, api_url="http://localhost:8000/process_prescription/"):
    # Ensure the image file exists
    if not Path(image_path).exists():
        print(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    
    # Prepare the file for upload
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/jpeg')}
            
            # Make the API request
            print(f"Sending image to {api_url}...")
            response = requests.post(api_url, files=files)
            
            # Check the response
            if response.status_code == 200:
                result = response.json()
                print("Successfully processed the prescription!")
                print("\nExtracted Medications:")
                
                # Display the extracted medications and dosages
                for i, item in enumerate(result.get('prescriptions', []), 1):
                    print(f"{i}. Medicine: {item['medicine']}")
                    print(f"   Dosage: {item['dosage']}")
                print("\nRaw API Response:")
                print(json.dumps(result, indent=2))
                return result
            else:
                print(f"Error: API returned status code {response.status_code}")
                print(f"Response: {response.text}")
                return None
    
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to the API at {api_url}")
        print("Make sure the API server is running and the URL is correct.")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return None

if __name__ == "__main__":
    # Check if an image path was provided
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <path_to_prescription_image>")
        sys.exit(1)
    
    # Get the image path from command line arguments
    image_path = sys.argv[1]
    
    # Test the API with the provided image
    test_prescription_api(image_path)