import requests
from io import BytesIO
from PIL import Image
import os

def get_favicon(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the domain from the URL
            domain = url.replace("https://", "").replace("http://", "").split("/")[0]
            
            # Try to find the favicon link in the HTML
            favicon_link = None
            for link in response.text.split("<link "):
                if "rel=\"icon\"" in link or "rel=\"shortcut icon\"" in link:
                    favicon_link = link.split("href=\"")[1].split("\"")[0]
                    break
            
            # If the favicon link was found, fetch the favicon
            if favicon_link:
                favicon_response = requests.get(favicon_link)
                if favicon_response.status_code == 200:
                    # Save the favicon to a file
                    favicon_file = os.path.join(os.getcwd(), f"{domain}.ico")
                    with open(favicon_file, "wb") as f:
                        f.write(favicon_response.content)
                    
                    # Return the favicon as a PIL Image object
                    return Image.open(BytesIO(favicon_response.content))
            else:
                # Try to fetch the default favicon location
                favicon_response = requests.get(f"{url}/favicon.ico")
                if favicon_response.status_code == 200:
                    # Save the favicon to a file
                    favicon_file = os.path.join(os.getcwd(), f"{domain}.ico")
                    with open(favicon_file, "wb") as f:
                        f.write(favicon_response.content)
                    
                    # Return the favicon as a PIL Image object
                    return Image.open(BytesIO(favicon_response.content))
    except requests.exceptions.RequestException:
        pass
    
    # If no favicon was found, return None
    return None

# Example usage
url = "https://www.wordpress.org"
favicon = get_favicon(url)
if favicon:
    print("Favicon successfully fetched!")
else:
    print("Failed to fetch favicon.")