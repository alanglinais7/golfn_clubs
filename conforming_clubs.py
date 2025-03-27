import requests
import time
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class USGAClubCollector:
    def __init__(self, base_url: str = "https://conformingclubandball-api-pd.azurewebsites.net"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'Accept': 'application/json',
            'Origin': 'https://equipmentdatabase.usga.org',
            'Content-Type': 'application/json'
        })
        
    def fetch_clubs(self, club_type: str = None, page_size: int = 100) -> List[Dict[Any, Any]]:
        """
        Fetches all clubs of a specific type from the USGA database
        
        Args:
            club_type: Type of club to fetch (e.g., "DRIVER", "IRON")
            page_size: Number of results per request
            
        Returns:
            List of club dictionaries
        """
        all_clubs = []
        page = 1
        
        while True:
            try:
                payload = {
                    "manufacturer": "",
                    "equipmentType": club_type,
                    "keyword": "",
                    "sortField": "Most Recent",
                    "searchPage": page
                }
                
                response = self.session.post(
                    f"{self.base_url}/search",
                    json=payload
                )
                response.raise_for_status()
                print(f"Request payload: {payload}")
                print(f"Response: {response.text[:500]}")
                
                clubs = response.json()
                
                if not clubs:
                    break
                    
                all_clubs.extend(clubs)
                print(f"Fetched page {page}, got {len(clubs)} clubs")
                
                page += 1
                time.sleep(1)  # Rate limiting
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {str(e)}")
                time.sleep(5)  # Back off on error
                continue
                
        return all_clubs
    
    def save_to_csv(self, clubs: List[Dict], filename: str = None):
        """Saves clubs data to CSV with proper handling of nested structures"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"usga_clubs_{timestamp}.csv"
            
        # Flatten markings into columns
        flattened_clubs = []
        for club in clubs:
            club_data = {k: v for k, v in club.items() if k != 'markings'}
            
            # Handle markings
            markings = club.get('markings', [])
            for marking in markings:
                header = marking.get('header', '').lower()
                value = marking.get('value', '')
                club_data[f'marking_{header}'] = value
                
            flattened_clubs.append(club_data)
            
        df = pd.DataFrame(flattened_clubs)
        df.to_csv(filename, index=False)
        print(f"Saved {len(clubs)} clubs to {filename}")

def main():
    collector = USGAClubCollector()
    
    # Example club types - you'll need to verify the exact values accepted by the API
    club_types = ["drivers", "fairway woods", "hybrids", "irons", "wedges"]
    
    all_clubs = []
    for club_type in club_types:
        print(f"\nCollecting {club_type}s...")
        clubs = collector.fetch_clubs(club_type)
        all_clubs.extend(clubs)
        
    collector.save_to_csv(all_clubs)

if __name__ == "__main__":
    main()