import pandas as pd

input_file = "input_files/input_file_id.xlsx"
output_file = 'output_files/output_file_id.csv'
output_file_no_duplicates = 'output_files/urls.csv'


def add_urls_to_excel(input_file_id, output_file_withurl):
    df = pd.read_excel(input_file_id)
    df['walmart_url'] = 'https://www.walmart.com/ip/' + df['item_id'].astype(str) + '?selected=true'
    df['comp_url'] = 'https://www.amazon.com/dp/' + df['retailer_id'].astype(str) + '?th=1&psc=1'
    df.to_csv(output_file_withurl, index=False)
    print(f"File '{output_file_withurl}' has been generated with Walmart and Comp URLs.")


def remove_duplicate_rows(input_file_withurl, output_removed_duplicates):
    if input_file_withurl.endswith('.xlsx'):
        df = pd.read_excel(input_file_withurl)
    elif input_file_withurl.endswith('.csv'):
        df = pd.read_csv(input_file_withurl)
    else:
        raise ValueError("Unsupported file format. Only Excel (.xlsx) and CSV (.csv) files are supported.")

    # Removing duplicates based on a combination of 'item_id' and 'retailer_id'
    df.drop_duplicates(subset=['item_id', 'retailer_id'], keep='first', inplace=True)

    if output_removed_duplicates.endswith('.xlsx'):
        df.to_excel(output_removed_duplicates, index=False)
    elif output_removed_duplicates.endswith('.csv'):
        df.to_csv(output_removed_duplicates, index=False)
    else:
        raise ValueError("Unsupported output file format. Only Excel (.xlsx) and CSV (.csv) files are supported.")

    print(f"Duplicate rows removed. File '{output_removed_duplicates}' has been generated.")


if __name__ == "__main__":
    add_urls_to_excel(input_file, output_file)
    remove_duplicate_rows(output_file, output_file_no_duplicates)
