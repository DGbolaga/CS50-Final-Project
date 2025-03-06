import pandas as pd

# Read the CSV files
updated_books = pd.read_csv('../csv_files/updated_books_with_covers.csv')
deleted_books = pd.read_csv('../csv_files/deleted_books.csv')

# Identify the key columns that define a unique book
key_columns = ['book_title', 'authors']  # Using the main identifying columns

# A.I: generated.
# Remove rows where the key columns match with deleted_books
updated_books_filtered = updated_books[~updated_books[key_columns].apply(tuple, axis=1).isin(
    deleted_books[key_columns].apply(tuple, axis=1)
)]

# Save the filtered dataframe to a new CSV file
updated_books_filtered.to_csv('csv_files/updated_books_without_errors.csv', index=False)



