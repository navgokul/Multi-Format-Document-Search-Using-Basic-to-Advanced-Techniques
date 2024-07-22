import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import shutil

# LLM Model Options
MODEL_OPTIONS = [
    "all-MiniLM-L6-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
    "all-MiniLM-L12-v2"
    "all-mpnet-base-v2"
    "multi-qa-MiniLM-L6-cos-v1"
    # Add more models here...
]

# Function to load and embed a single document
def load_and_embed_document(filepath, model):
    if filepath.endswith('.pdf'):
        return load_pdf(filepath, model)
    elif filepath.endswith(('.png', '.jpg', '.jpeg')):
        return load_image(filepath, model)
    elif filepath.endswith('.txt'):
        return load_text_file(filepath, model)
    else:
        return None

# Load functions for different document types
def load_pdf(filepath, model):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

def load_image(filepath, model):
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

def load_text_file(filepath, model):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

# Function to extract metadata from a file
def get_metadata(filepath):
    return {
        'filename': os.path.basename(filepath),
        'size': os.path.getsize(filepath),
        'creation_date': os.path.getctime(filepath)
    }

# Function to create a Faiss index from document embeddings
def create_index(documents):
    dimension = len(documents[0]['embedding'])
    index = faiss.IndexFlatL2(dimension)
    embeddings = np.array([doc['embedding'] for doc in documents])
    index.add(embeddings)
    return index

# Function to search the Faiss index for similar documents
def search_index(index, query_embedding, metadata, top_k=5):
    distances, indices = index.search(np.array([query_embedding]), top_k)
    results = []
    for i in range(top_k):
        result = metadata[indices[0][i]]
        result['distance'] = distances[0][i]
        results.append(result)
    return results

# --- Tkinter UI ---
def browse_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

def browse_destination():
    directory = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, directory)

def run_search():
    query = query_entry.get("1.0", tk.END).strip()
    selected_model = model_var.get()
    destination_folder = destination_entry.get()

    if not query or not directory_entry.get() or not destination_folder:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a query, select source directory, and destination folder.")
        return

    # Load Model
    model = SentenceTransformer(selected_model)

    # Load Documents with Progress Bar
    document_directory = directory_entry.get()
    filepaths = [os.path.join(document_directory, filename) for filename in os.listdir(document_directory)]
    documents = []
    for fp in tqdm(filepaths, desc="Loading Documents"):
        doc = load_and_embed_document(fp, model)
        if doc:
            documents.append(doc)

    # Create Index
    index = create_index(documents)
    metadata = [doc['metadata'] for doc in documents]

    # Search
    query_embedding = model.encode(query)
    results = search_index(index, query_embedding, metadata)

    # Display Results and Copy Files
    result_text.delete("1.0", tk.END)
    for result in results:
        result_text.insert(tk.END, f"Filename: {result['filename']}\n")
        result_text.insert(tk.END, f"Distance: {result['distance']:.4f}\n\n")

        # Copy the file to the destination folder
        source_filepath = os.path.join(document_directory, result['filename'])
        destination_filepath = os.path.join(destination_folder, result['filename'])
        try:
            shutil.copy2(source_filepath, destination_filepath)  # Copy with metadata
        except Exception as e:
            messagebox.showerror("Error Copying File", f"Could not copy {result['filename']}: {str(e)}")

def main():
    # Create main window
    root = tk.Tk()
    root.title("Semantic Document Search")

    # Directory Selection
    directory_label = tk.Label(root, text="Source Directory:")
    directory_label.grid(row=0, column=0, padx=5, pady=5)

    directory_entry = tk.Entry(root, width=50)
    directory_entry.grid(row=0, column=1, padx=5, pady=5)

    browse_button = tk.Button(root, text="Browse", command=browse_directory)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    # Destination Folder Selection
    destination_label = tk.Label(root, text="Destination Folder:")
    destination_label.grid(row=1, column=0, padx=5, pady=5)

    destination_entry = tk.Entry(root, width=50)
    destination_entry.grid(row=1, column=1, padx=5, pady=5)

    browse_destination_button = tk.Button(root, text="Browse", command=browse_destination)
    browse_destination_button.grid(row=1, column=2, padx=5, pady=5)

    # Model Selection
    model_label = tk.Label(root, text="Select Model:")
    model_label.grid(row=2, column=0, padx=5, pady=5)

    model_var = tk.StringVar(root)
    model_var.set(MODEL_OPTIONS[0])  # Default model

    model_dropdown = tk.OptionMenu(root, model_var, *MODEL_OPTIONS)
    model_dropdown.grid(row=2, column=1, padx=5, pady=5)

    # Query Input
    query_label = tk.Label(root, text="Enter your query:")
    query_label.grid(row=3, column=0, padx=5, pady=5)

    query_entry = tk.Text(root, height=3)
    query_entry.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    # Search Button
    search_button = tk.Button(root, text="Search", command=run_search)
    search_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    # Results
    result_label = tk.Label(root, text="Search Results:")
    result_label.grid(row=6, column=0, padx=5, pady=5)

    result_text = tk.Text(root, wrap=tk.WORD)
    result_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
