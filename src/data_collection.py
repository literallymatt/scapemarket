import requests
import yaml
import json
from pathlib import Path
import time

def load_config(config_path="config.yaml"):
    """Loads the YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def fetch_timeseries_data(item_id: int, timestep: str, api_config: dict) -> dict:
    """Fetches timeseries data for a given item from the OSRS Wiki API."""
    headers = {'User-Agent': api_config['user_agent']}
    params = {'id': item_id, 'timestep': timestep}
    url = f"{api_config['base_url']}{api_config['timeseries_endpoint']}"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request failed for item {item_id}: {e}")
        return None

def save_raw_data(data: dict, item_name: str, timestep: str, raw_data_path: Path):
    """Saves the fetched data to a JSON file in the raw data directory."""
    if not data:
        print(f"No data to save for {item_name}.")
        return

    raw_data_path.mkdir(parents=True, exist_ok=True)
    safe_item_name = item_name.lower().replace(' ', '_')
    output_file = raw_data_path / f"{safe_item_name}_{timestep}.json"

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully saved data for {item_name} to {output_file}")

def run_collection():
    """Main function to run the data collection process."""
    print("Starting data collection...")
    config = load_config()
    api_config = config['api']
    items_to_track = config['items']
    data_path = Path(config['settings']['data_path'])
    raw_data_path = data_path / "raw"
    timestep = config['settings']['timestep']

    for item in items_to_track:
        print(f"Fetching data for {item['name']} (ID: {item['id']})...")
        price_data = fetch_timeseries_data(item['id'], timestep, api_config)
        if price_data:
            save_raw_data(price_data, item['name'], timestep, raw_data_path)
        time.sleep(1) # Be a good API citizen
    print("Data collection finished.")