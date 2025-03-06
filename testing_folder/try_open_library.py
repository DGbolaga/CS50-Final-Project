import pandas as pd
import requests

def fetch_open_library_cover(book_title, authors):
    """
    Fetches cover image URL from Open Library based on book title and authors.
    """
    # AI: generated validation logic

    base_url = "https://openlibrary.org/search.json"
    params = {"title": book_title, "author": authors}
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("docs"):
                for doc in data["docs"]:
                    if "cover_i" in doc:  # Check if cover image exists
                        cover_id = doc["cover_i"]
                        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
        return None
    except requests.RequestException as e:
        print(f"Error fetching data for '{book_title}' by {authors}: {e}")
        return None

def update_book_covers(file_path, output_path):
    """
    Reads a CSV file, updates cover images using Open Library API, and saves the result.
    A.I: assistance used.
    """

    print("Loading book data...")
    books_df = pd.read_csv(file_path)
    updated_covers = []
    
    print(f"Processing {len(books_df)} books...")
    for index, row in books_df.iterrows():
        title = row["book_title"]
        authors = row["authors"]
        current_cover = row["cover_img"]

        print(f"[{index + 1}/{len(books_df)}] Searching for updated cover for '{title}' by {authors}...")
        
        # Fetch updated cover
        new_cover = fetch_open_library_cover(title, authors)
        if new_cover:
            print(f" - Updated cover found: {new_cover}")
        else:
            print(f" - No updated cover found. Keeping current cover.")

        updated_covers.append(new_cover if new_cover else current_cover)

    # Add updated covers to the DataFrame
    books_df["updated_cover_img"] = updated_covers
    
    print("Saving updated book data...")
    books_df.to_csv(output_path, index=False)
    print(f"Updated book covers saved to {output_path}")

if __name__ == "__main__":
    # Input and output file paths
    input_file = "updated_books_one.csv"
    output_file = "updated_books_with_covers.csv"
    
    # Update book covers
    print("Starting book cover update process...")
    update_book_covers(input_file, output_file)
    print("Book cover update process completed.")
