from src.data_ingestion import load_all_data
from src.data_cleaning import clean_merge_people, clean_promotion_csv, clean_transfers_csv, clean_trasactions_xml, create_filtered_csv
from src.data_analysis import transactions_filtered_analysis, transfers_filtered_analysis, promotions_filtered_analysis

def main():
    
    # Load all data
    file_path = "./data"
    trasactions_xml, people_yamal, promotion_csv, transfer_csv, people_json  = load_all_data(file_path)

    # FUNCTIONS --------------------------------------------
    df_people = clean_merge_people(people_yamal, people_json)
    df_people_filtered, df_promotions_filtered = clean_promotion_csv(df_people, promotion_csv)
    df_transfers_filtered = clean_transfers_csv(df_people_filtered, transfer_csv)
    df_transactions_filtered = clean_trasactions_xml(df_people_filtered, trasactions_xml)
    create_filtered_csv(df_people_filtered, df_promotions_filtered, df_transfers_filtered, df_transactions_filtered)
    # FUNCTIONS --------------------------------------------
    
    print(transactions_filtered_analysis())
    print(transfers_filtered_analysis())
    print(promotions_filtered_analysis())
    
    return 

if __name__ == "__main__":
    main()