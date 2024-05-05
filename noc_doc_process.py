import sqlite3
import pandas as pd

def load_table_from_database(db_path, table_name):
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def create_document_dataframe(original_df):
    new_df = pd.DataFrame(columns=['noc', 'document'])

    for index, row in original_df.iterrows():
        # Concatenate strings from all columns except 'noc' and 'url'
        document = '\n \n '.join(row[col] for col in original_df.columns if col not in ['noc', 'url'])
        
        # Append the 'noc' and 'document' to the new DataFrame
        new_df = new_df._append({'noc': row['noc'], 'document': document}, ignore_index=True)

    return new_df

if __name__ == "__main__":
    db_path = "data/unit_groups.db"
    table_name = "unit_groups"
    output_file_path = "data/noc_docs.csv"

    data_frame = load_table_from_database(db_path, table_name)
    new_dataframe = create_document_dataframe(data_frame)
    new_dataframe.to_csv(output_file_path, index=False)
