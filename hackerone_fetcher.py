#!/usr/bin/env python3
import requests
import argparse
import json
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_all_programs(username, api_key):
    """
    Fetches all programs from the HackerOne API, handling pagination.
    """
    url = "https://api.hackerone.com/v1/hackers/programs"
    programs = []
    page_number = 1
    
    while True:
        logging.info(f"Fetching page {page_number}...")
        try:
            response = requests.get(
                url,
                auth=(username, api_key),
                params={"page[number]": page_number, "page[size]": 100}
            )
            response.raise_for_status()
            data = response.json()
            
            current_page_programs = data.get('data', [])
            programs.extend(current_page_programs)
            
            if not current_page_programs or len(current_page_programs) < 100:
                break
                
            page_number += 1
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching programs on page {page_number}: {e}")
            if response.status_code == 401:
                 logging.error("Authentication failed. Please check your Username and API Key.")
            break
            
    return programs

def filter_programs(programs, program_type):
    """
    Filters programs based on the specified type.
    """
    if not program_type or program_type == 'all':
        return programs
        
    filtered_programs = []
    for program in programs:
        attributes = program.get('attributes', {})
        offers_bounties = attributes.get('offers_bounties')
        
        if program_type == 'bounty':
            if offers_bounties:
                filtered_programs.append(program)
        elif program_type == 'vdp':
             if not offers_bounties:
                filtered_programs.append(program)
        # Add more specific filtering logic here if needed based on API response structure
        
    return filtered_programs

def main():
    parser = argparse.ArgumentParser(description="Fetch HackerOne programs.")
    parser.add_argument("username", help="HackerOne API Username (Identifier)")
    parser.add_argument("api_key", help="HackerOne API Key (Token)")
    parser.add_argument("--type", choices=['all', 'bounty', 'vdp'], default='all', help="Filter programs by type (default: all)")
    parser.add_argument("--output", default="programs.json", help="Output JSON file name")

    args = parser.parse_args()

    logging.info("Starting HackerOne Program Fetcher")
    
    all_programs = get_all_programs(args.username, args.api_key)
    logging.info(f"Total programs fetched: {len(all_programs)}")
    
    filtered_programs = filter_programs(all_programs, args.type)
    logging.info(f"Programs after filtering ({args.type}): {len(filtered_programs)}")
    
    if filtered_programs:
        with open(args.output, 'w') as f:
            json.dump(filtered_programs, f, indent=4)
        logging.info(f"Results saved to {args.output}")
    else:
        logging.warning("No programs found matching the criteria.")

if __name__ == "__main__":
    main()
