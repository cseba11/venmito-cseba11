import os
import numpy as np
import pandas as pd
import yaml
import xml.etree.ElementTree as ET

# Function for the XML file type
def parse_transactions(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Array to stored the data from the XML file
    data = []
    
    # Iterate over each transaction in the XML file
    for transaction in root.findall('transaction'):
        transaction_id = transaction.get('id')  # Get the transaction ID
        phone = transaction.find('phone').text  # Get the phone number
        store = transaction.find('store').text  # Get name of the store


        for item in transaction.find('items').findall('item'):
            item_name = item.find('item').text
            price = float(item.find('price').text)
            price_per_item = float(item.find('price_per_item').text)
            quantity = int(item.find('quantity').text)

            # Add data to the data array 
            data.append({
                'transaction_id': transaction_id,
                'phone': phone,
                'store': store,
                'item': item_name,
                'price': price,
                'price_per_item': price_per_item,
                'quantity': quantity
            })

    # Convert the data array to a DataFrame and return it
    return pd.DataFrame(data)


def load_all_data(data_dir):
    data_frames = []
    
    # Iterate over all files in the data directory
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        
        if file.endswith(".csv"):
            df = pd.read_csv(file_path)
            data_frames.append(df)
            
        elif file.endswith(".json"):
            df = pd.read_json(file_path)
            data_frames.append(df)
            
        elif file.endswith(".yaml") or file.endswith(".yml"):
            with open(file_path, 'r') as f:
                yaml_data = yaml.safe_load(f)
                # Convert the YAML data to a DataFrame
                df = pd.json_normalize(yaml_data) if isinstance(yaml_data, list) else pd.DataFrame([yaml_data])
                data_frames.append(df)
                
        elif file.endswith(".xml"):
            # Call the function to parse the XML file
            df = parse_transactions(file_path)
            data_frames.append(df)
    
    return data_frames

