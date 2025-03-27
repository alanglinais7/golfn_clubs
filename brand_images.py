import os
import requests
import time
from serpapi import GoogleSearch
import pandas as pd
from dotenv import load_dotenv  # You'll need to install: pip install python-dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("SERPAPI_KEY")  # Store in .env file instead of hardcoding
OUTPUT_FOLDER = "brand_logos"
CSV_FILE_PATH = "golfn-app-brands.csv"
UPDATED_CSV_PATH = "golfnappbrands_updated.csv"

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def search_and_download_logo(brand_name, brand_id):
    """
    Search for a brand logo and download the first result
    Returns True if successful, False otherwise
    """
    try:
        # Construct search query with size and transparency parameters
        params = {
            "engine": "google_images",
            "q": f"{brand_name} golf logo",
            "tbm": "isch",
            "api_key": API_KEY,
            "imgsz": "2mp",       # Larger than 2MP images
            "image_color": "trans" # Transparent images
        }
        
        # Execute search
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Check if we got any image results
        if "images_results" in results and len(results["images_results"]) > 0:
            # Get the first image result
            first_result = results["images_results"][0]
            image_url = first_result["original"]
            
            # Download the image
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                # Clean filename - remove special characters
                clean_name = ''.join(c if c.isalnum() else '_' for c in brand_name)
                
                # Get file extension from content-type or URL
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = 'jpg'
                elif 'png' in content_type:
                    ext = 'png'
                elif 'gif' in content_type:
                    ext = 'gif'
                else:
                    # Default to jpg if can't determine
                    ext = 'jpg'
                
                filename = f"{brand_id}_{clean_name}.{ext}"
                filepath = os.path.join(OUTPUT_FOLDER, filename)
                
                # Save the image
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                        
                print(f"✅ Downloaded logo for {brand_name}")
                return True
            else:
                print(f"❌ Failed to download image for {brand_name} (HTTP {response.status_code})")
                return False
        else:
            print(f"❌ No image results found for {brand_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {brand_name}: {str(e)}")
        return False

def process_brands():
    """
    Process all brands in the CSV file
    """
    try:
        # Check if CSV file exists
        if not os.path.exists(CSV_FILE_PATH):
            print(f"❌ CSV file not found: {CSV_FILE_PATH}")
            return
            
        # Read the CSV file
        df = pd.read_csv(CSV_FILE_PATH)
        
        # Check if 'Updated' column exists, if not add it
        if 'Updated' not in df.columns:
            df['Updated'] = False
        
        # Initialize count variables
        total_brands = len(df)
        successful = 0
        failed = 0
        
        # Process each brand
        for index, row in df.iterrows():
            brand_id = row['BrandID']
            brand_name = row['Brand Name']
            already_updated = row.get('Updated', False)  # Use get() with default value
            
            # Skip if already processed
            if already_updated:
                print(f"⏩ Skipping {brand_name} (already processed)")
                continue
            
            print(f"🔍 Processing {brand_name} ({index+1}/{total_brands})")
            
            # Search and download
            success = search_and_download_logo(brand_name, brand_id)
            
            # Update status
            df.at[index, 'Updated'] = success
            
            # Update counts
            if success:
                successful += 1
            else:
                failed += 1
            
            # Save progress periodically (every 10 brands)
            if (index + 1) % 10 == 0:
                df.to_csv(UPDATED_CSV_PATH, index=False)
                print(f"💾 Progress saved to {UPDATED_CSV_PATH}")
            
            # Delay to avoid hitting API rate limits (3 seconds)
            time.sleep(3)
        
        # Save final results
        df.to_csv(UPDATED_CSV_PATH, index=False)
        
        # Print summary
        print(f"\n✅ Process complete!")
        print(f"Total brands: {total_brands}")
        print(f"Successfully downloaded: {successful}")
        print(f"Failed: {failed}")
    
    except Exception as e:
        print(f"❌ Error processing CSV: {str(e)}")

if __name__ == "__main__":
    if not API_KEY:
        print("❌ API key not found. Please set SERPAPI_KEY in your .env file.")
    else:
        process_brands()