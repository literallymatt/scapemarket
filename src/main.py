import argparse
from pathlib import Path
import yaml
import pandas as pd

# We import our custom modules
from . import data_collection
# The following are placeholders for when you create them
# from src import feature_engineering, model_training, predict

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="RuneScape GE Price Predictor")
    parser.add_argument(
        "action",
        choices=["collect", "process", "train", "predict", "all"],
        help="The action to perform."
    )
    args = parser.parse_args()

    # Load config to get paths and item info
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    data_path = Path(config['settings']['data_path'])
    raw_path = data_path / "raw"
    processed_path = data_path / "processed"
    model_path = Path("models") # A dedicated folder for models

    if args.action in ["collect", "all"]:
        data_collection.run_collection()

    if args.action in ["process", "all"]:
        print("\nProcessing step is not yet implemented.")
        # Placeholder for future logic:
        # for raw_file in raw_path.glob("*.json"):
        #     feature_engineering.process_and_save_features(raw_file, processed_path)

    if args.action in ["train", "all"]:
        print("\nTraining step is not yet implemented.")
        # Placeholder for future logic:
        # for processed_file in processed_path.glob("*.csv"):
        #     model_training.train_model(processed_file, model_path)

    if args.action in ["predict", "all"]:
        print("\nPrediction step is not yet implemented.")
        # Placeholder for future logic:
        # for model_file in model_path.glob("*.joblib"):
        #     predict.make_prediction(...)

if __name__ == "__main__":
    main()