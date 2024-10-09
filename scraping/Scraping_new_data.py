import pandas as pd

base_file_path = "D:\\Downloads\\"

def load_first_two_rows_with_rename(file_name, rename_dict):
    file_path = base_file_path + file_name
    df = pd.read_excel(file_path)
    df = df.iloc[:2]
    columns_to_keep = ['Date'] + list(rename_dict.keys())
    df = df[columns_to_keep]
    df = df.rename(columns=rename_dict)
    df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
    
    for col in list(rename_dict.values()):
        df[col] = df[col].astype(str).str.replace(',', '').str.replace('%', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

datasets_info = [
    ('BSE.xlsx', {'Price': 'BSE Price'}),
    ('Bond-Price.xlsx', {'Price': 'Bond Price'}),
    ('Crude-Oil.xlsx', {'Price': 'Crude Price'}),
    ('Gold-Price.xlsx', {'Price': 'Gold Price', 'Change': 'Gold Change %'}),
    ('Nifty.xlsx', {'Price': 'Nifty Price'}),
    ('Silver-price.xlsx', {'Price': 'Silver Price'}),
    ('USD-INR.xlsx', {'Price': 'USD/INR'})
]

first_two_rows = [load_first_two_rows_with_rename(file_name, rename_dict) 
                  for file_name, rename_dict in datasets_info]

merged_df = pd.concat(first_two_rows, axis=1)
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

merged_df['Repo Rate'] = 6.5
merged_df['WPI'] = 0.01

merged_df = merged_df.sort_values(by='Date', ascending=True)


dataset_xlsx_path = "C:\\Users\\yasee\\Desktop\\Kauser\\goldprice\\dataset.xlsx"
dataset_xlsx = pd.read_excel(dataset_xlsx_path)


final_df = pd.concat([dataset_xlsx, merged_df], ignore_index=True)

final_df.to_excel('final_merged_dataset.xlsx', index=False)
print(final_df.tail(4))

