import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, Text, END
import shutil

# Load documents from a directory, handling different file types (PDF, image, text)
def load_documents(directory):
    documents = []
    skipped_files = []  # Store files that caused errors
    for filename in tqdm(os.listdir(directory), desc="Loading Documents"):
        filepath = os.path.join(directory, filename)
        try:
            if filename.endswith('.pdf'):
                documents.append(load_pdf(filepath))
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                documents.append(load_image(filepath))
            elif filename.endswith('.txt'):
                documents.append(load_text_file(filepath))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            skipped_files.append(filename)  # Add problematic file to the list
    return documents, skipped_files

# Load and process a PDF file, extracting its text content
def load_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return {'text': text, 'metadata': get_metadata(filepath)}

# Load and process an image file, extracting text using OCR (pytesseract)
def load_image(filepath):
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)
    return {'text': text, 'metadata': get_metadata(filepath)}

# Load and process a text file, reading its content
def load_text_file(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
    return {'text': text, 'metadata': get_metadata(filepath)}

# Extract metadata from a file, including filename, size, and creation date
def get_metadata(filepath):
    return {
        'filename': os.path.basename(filepath),
        'size': os.path.getsize(filepath),
        'creation_date': os.path.getctime(filepath)
    }

# Create an index from the loaded documents using Whoosh
def create_index(directory, documents):
    schema = Schema(filename=ID(stored=True),
                    size=STORED,
                    creation_date=STORED,
                    content=TEXT(analyzer=StemmingAnalyzer()))

    if not os.path.exists(directory):
        os.mkdir(directory)

    index = create_in(directory, schema)
    writer = index.writer()

    for doc in tqdm(documents, desc="Indexing"):
        writer.add_document(filename=doc['metadata']['filename'],
                            size=doc['metadata']['size'],
                            creation_date=doc['metadata']['creation_date'],
                            content=doc['text'])
    writer.commit()

# Search the index for a given query string and return matching documents' filenames
def search_index(directory, query_str):
    index = open_dir(directory)
    query = QueryParser("content", index.schema).parse(query_str)
    with index.searcher() as searcher:
        results = searcher.search(query)
        return [{'filename': result['filename']} for result in results]  # Return only filenames

# Main function to set up the GUI and handle user interactions
def main():
    # Select source folder for documents
    def select_source_folder():
        folder_selected = filedialog.askdirectory()
        source_folder_entry.delete(0, END)
        source_folder_entry.insert(0, folder_selected)

    # Select destination folder for copying search results
    def select_destination_folder():
        folder_selected = filedialog.askdirectory()
        destination_folder_entry.delete(0, END)
        destination_folder_entry.insert(0, folder_selected)

    # Start indexing process
    def start_indexing():
        document_directory = source_folder_entry.get()
        index_directory = "indexdir"
        documents, skipped_files = load_documents(document_directory)
        create_index(index_directory, documents)

        if skipped_files:
            error_message = "The following files were skipped due to errors:\n\n" + "\n".join(skipped_files)
            tk.messagebox.showwarning("Skipped Files", error_message)

    # Search the index and copy matching documents to the destination folder
    def search_and_copy():
        document_directory = source_folder_entry.get()
        index_directory = "indexdir"
        destination_directory = destination_folder_entry.get()
        query = search_entry.get("1.0", END).strip()

        results = search_index(index_directory, query)
        for result in results:
            source_path = os.path.join(document_directory, result['filename'])
            destination_path = os.path.join(destination_directory, result['filename'])
            shutil.copy2(source_path, destination_path)
            print(result)

    # --- GUI ---
    window = tk.Tk()
    window.title("Document Search Engine")

    # Source folder selection
    source_folder_label = tk.Label(window, text="Source Folder:")
    source_folder_label.grid(row=0, column=0, padx=5, pady=5)

    source_folder_entry = tk.Entry(window, width=50)
    source_folder_entry.grid(row=0, column=1, padx=5, pady=5)

    source_folder_button = tk.Button(window, text="Browse", command=select_source_folder)
    source_folder_button.grid(row=0, column=2, padx=5, pady=5)

    # Destination folder selection
    destination_folder_label = tk.Label(window, text="Destination Folder:")
    destination_folder_label.grid(row=1, column=0, padx=5, pady=5)

    destination_folder_entry = tk.Entry(window, width=50)
    destination_folder_entry.grid(row=1, column=1, padx=5, pady=5)

    destination_folder_button = tk.Button(window, text="Browse", command=select_destination_folder)
    destination_folder_button.grid(row=1, column=2, padx=5, pady=5)

    # Index documents button
    index_button = tk.Button(window, text="Index Documents", command=start_indexing)
    index_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Search label and entry
    search_label = tk.Label(window, text="Search:")
    search_label.grid(row=3, column=0, padx=5, pady=5)

    search_entry = Text(window, height=2, width=40)
    search_entry.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    # Search and copy button
    search_button = tk.Button(window, text="Search and copy", command=search_and_copy)
    search_button.grid(row=5, column=0, columnspan=3, pady=10)

    window.mainloop()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
