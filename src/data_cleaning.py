import os
import numpy as np
import pandas as pd

def clean_merge_people(people_yamal, people_json):
    
    # Create df_people with the similar information from people_yamal and people_json
    combined = pd.concat([people_json, people_yamal], ignore_index=True)

    df_unique = combined.drop_duplicates(subset='id', keep='first')
    df_unique = df_unique.sort_values(by='id')

    # Change the column 'location' to 'city' and 'country' to have a better uniform data
    df_unique['city'] = df_unique.apply(
        lambda row: f"{row['location']['City']}, {row['location']['Country']}"
        if pd.isna(row['city']) and isinstance(row['location'], dict) else row['city'], 
        axis=1
    )

    # Change the column 'name' to 'first_name' and 'last_name' to have a better uniform data
    df_unique['first_name'] = df_unique.apply(
        lambda row: row['name'].split()[0] if pd.notna(row['name']) else row['first_name'], axis=1
    )

    df_unique['last_name'] = df_unique.apply(
        lambda row: ' '.join(row['name'].split()[1:]) if pd.notna(row['name']) else row['last_name'], axis=1
    )

    # Change the column 'phone' to 'telephone'
    df_unique['telephone'] = df_unique.apply(
        lambda row: row['phone'] if pd.notna(row['phone']) else row['telephone'], axis=1
    )

    # Change the column 'devices' to only have 'Android', 'Desktop' and 'Iphone' 
    df_unique['Android'] = df_unique['devices'].apply(lambda d: d.count('Android') if isinstance(d, list) else 0.0)
    df_unique['Desktop'] = df_unique['devices'].apply(lambda d: d.count('Desktop') if isinstance(d, list) else 0.0)
    df_unique['Iphone'] = df_unique['devices'].apply(lambda d: d.count('Iphone') if isinstance(d, list) else 0.0)

    # Drop the columns 'location', 'name' and 'phone' because they are not needed anymore
    df_unique = df_unique.drop(columns=['location'])
    df_unique = df_unique.drop(columns=['name'])
    df_unique = df_unique.drop(columns=['phone'])
    df_people = df_unique.drop(columns=['devices'])

    return df_people


def clean_promotion_csv(df_people, promotion_csv):
    df_promotions = promotion_csv.rename(columns={'id': 'promotion_id'})

    # Merge both tables on "email" and "telephone"
    df_temp_1 = pd.merge(df_people, df_promotions, on='telephone', how='inner')


    df_promotions = df_promotions.rename(columns={'client_email': 'email'})
    
    # Drop the column 'telephone' to avoid telephone_x and "telephone_y" columns after the merge
    df_promotions = df_promotions.drop(columns=['telephone'])
    df_temp_2 = pd.merge(df_people, df_promotions, on='email', how='inner')
    
    # Merge both temp df on email 
    df_merge_promotion_people = pd.merge(df_temp_1, df_temp_2, on='email', how='outer')

    # Iterate over columns ending with '_x'
    for col in df_merge_promotion_people.columns:
        if col.endswith('_x'):
            # Corresponding column name in '_y'
            col_y = col.replace('_x', '_y')
            if col_y in df_merge_promotion_people.columns:
                # Update the '_x' column with values from '_y' if '_x' is NaN
                df_merge_promotion_people[col] = np.where(
                    df_merge_promotion_people[col].isna(),
                    df_merge_promotion_people[col_y],
                    df_merge_promotion_people[col]
                )

    # Remove '_y' columns after updating
    columns_to_drop = [col for col in df_merge_promotion_people.columns if col.endswith('_y')]
    df_merge_promotion_people = df_merge_promotion_people.drop(columns=columns_to_drop)


    # Rename columns that have '_x' suffix to remove it
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'id_x': 'id'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'first_name_x': 'first_name'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'last_name_x': 'last_name'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'telephone_x': 'telephone'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'Android_x': 'Android'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'Desktop_x': 'Desktop'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'Iphone_x': 'Iphone'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'city_x': 'city'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'promotion_id_x': 'promotion_id'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'promotion_x': 'promotion'})
    df_merge_promotion_people = df_merge_promotion_people.rename(columns={'responded_x': 'responded'})
    
    df_merge_promotion_people = df_merge_promotion_people.drop(columns=['client_email'])

    # Drop rows with NaN values
    df_merge_promotion_people = df_merge_promotion_people.dropna()

    df_people_filtered = df_people[df_people['id'].isin(df_merge_promotion_people['id'])]
    df_promotions_filtered = df_promotions[df_promotions['email'].isin(df_merge_promotion_people['email'])]
    
    return (df_people_filtered, df_promotions_filtered)

def clean_transfers_csv(df_people_filtered, transfer_csv):
    valid_transfers_filtered = transfer_csv.copy()
    valid_transfers_filtered['in_df_people_filtered'] = valid_transfers_filtered.apply(
        lambda row: row['sender_id'] in df_people_filtered['id'].values and row['recipient_id'] in df_people_filtered['id'].values,
        axis=1
    )

    df_transfers_filtered = valid_transfers_filtered[valid_transfers_filtered['in_df_people_filtered']]
    df_transfers_filtered = df_transfers_filtered.drop(columns=['in_df_people_filtered'])
    
    return df_transfers_filtered

def clean_trasactions_xml(df_people_filtered, trasactions_xml):
    
    # Filter transactions where 'phone' matches 'telephone' in df_people_filtered
    df_transactions_filtered = trasactions_xml[trasactions_xml['phone'].isin(df_people_filtered['telephone'])]

    return df_transactions_filtered

def create_filtered_csv(df_people_filtered, df_promotions_filtered, df_transfers_filtered, df_transactions_filtered):
    filtered_dataframes = [
        (df_people_filtered, 'people_filtered.csv'),
        (df_promotions_filtered, 'promotions_filtered.csv'),
        (df_transfers_filtered, 'transfers_filtered.csv'),
        (df_transactions_filtered, 'transactions_filtered.csv')
    ]

    # Path for the folder where the processed files will be saved
    processed_folder = "./data/processed"



    # Save each DataFrame as a CSV file in the "processed" folder
    for df, filename in filtered_dataframes:
        file_path = os.path.join(processed_folder, filename)
        df.to_csv(file_path, index=False)  
        
    return 

