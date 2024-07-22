import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, Index, ServerlessSpec  # Import Pinecone and Index
import json
from tqdm import tqdm  # For progress bars
from typing import List, Dict  # For type hinting
import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, RIGHT, Y, BOTTOM, X, TOP, NONE
import threading

# --- Configuration ---
PINECONE_API_KEY = 'YOUR_API_KEY'  # Replace with your Pinecone API key
PINECONE_ENVIRONMENT = 'us-west1-gcp'  # Replace with your Pinecone environment
INDEX_NAME = 'document-index'
DEFAULT_LLM_MODEL = 'all-MiniLM-L6-v2'
# ---------------------

# --- Global Variables ---
index = None  # Initialize Pinecone index globally
model = SentenceTransformer(DEFAULT_LLM_MODEL)  # Load default LLM model

# --- UI Functions ---
def select_document_directory():
    """Opens a directory selection dialog and updates the directory path."""
    directory = filedialog.askdirectory()
    document_directory_entry.delete(0, tk.END)
    document_directory_entry.insert(0, directory)

def update_status(message):
    """Updates the status label with the given message."""
    status_label.config(text=message)

def process_documents():
    """Loads, processes, and indexes documents in a separate thread."""
    def thread_function():
        try:
            update_status("Loading documents...")
            document_directory = document_directory_entry.get()
            documents = load_documents(document_directory)

            update_status("Creating index...")
            global index
            index = initialize_pinecone()
            create_index(index, documents)

            update_status("Indexing complete!")
        except Exception as e:
            update_status(f"Error: {e}")

    threading.Thread(target=thread_function).start()

def search_documents():
    """Searches the index based on the user's query."""
    query = search_entry.get("1.0", tk.END).strip()
    if query:
        try:
            search_results.delete("1.0", tk.END)
            search_index(index, query)
        except Exception as e:
            search_results.insert(tk.END, f"Error: {e}")

# --- LLM Model Selection ---
def select_llm_model(model_name: str):
    global selected_model
    selected_model = model_name

# --- Document Loading Functions ---
def load_documents(directory: str) -> List[Dict]:
    """Loads documents from the specified directory, handling various file types."""
    documents = []
    for filename in tqdm(os.listdir(directory), desc="Loading Documents"):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.pdf'):
            documents.append(load_pdf(filepath))
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            documents.append(load_image(filepath))
        elif filename.endswith('.txt'):
            documents.append(load_text_file(filepath))
    return documents

def load_pdf(filepath: str) -> Dict:
    """Loads and processes a PDF file."""
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

def load_image(filepath: str) -> Dict:
    """Loads and processes an image file."""
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

def load_text_file(filepath: str) -> Dict:
    """Loads and processes a text file."""
    with open(filepath, 'r') as file:
        text = file.read()
    embedding = model.encode(text)
    return {'text': text, 'embedding': embedding, 'metadata': get_metadata(filepath)}

def get_metadata(filepath: str) -> Dict:
    """Extracts metadata from a file."""
    return {
        'filename': os.path.basename(filepath),
        'size': os.path.getsize(filepath),
        'creation_date': os.path.getctime(filepath)
    }

# --- Pinecone Index Management ---
def initialize_pinecone():
    """Initializes the Pinecone connection."""
    pinecone = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)  # Create Pinecone instance
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=len(model.encode("test text")),
                              spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    return pinecone.Index(INDEX_NAME)  # Get the index object

def create_index(index: Index, documents: List[Dict]):
    """Creates or updates the Pinecone index with document embeddings."""
    for i, doc in enumerate(tqdm(documents, desc="Creating Index")):
        metadata = json.dumps(doc['metadata'])
        index.upsert([(str(i), doc['embedding'].tolist(), {'metadata': metadata})])

# --- Search Functionality (Modified to update UI) ---
def search_index(index, query_str: str, top_k: int = 5) -> None:
    """Searches the Pinecone index and updates the search results text area."""
    query_embedding = model.encode(query_str).tolist()
    
    # Correct the query call here:
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True) 

    if results['matches']:
        for result in results['matches']:
            metadata = json.loads(result['metadata']['metadata'])
            score = result['score']
            search_results.insert(tk.END, f"Filename: {metadata['filename']}\n")
            search_results.insert(tk.END, f"Score: {score:.4f}\n\n")
    else:
        search_results.insert(tk.END, "No matching documents found.\n")

# --- Tinker Integration (Example) - Not implemented in UI ---
# ... (Code from previous response)

# --- UI Setup ---
root = tk.Tk()
root.title("Document Search App")

# --- Document Directory Selection ---
document_directory_label = tk.Label(root, text="Document Directory:")
document_directory_label.grid(row=0, column=0, padx=5, pady=5)

document_directory_entry = tk.Entry(root, width=50)
document_directory_entry.grid(row=0, column=1, padx=5, pady=5)

document_directory_button = tk.Button(root, text="Browse", command=select_document_directory)
document_directory_button.grid(row=0, column=2, padx=5, pady=5)

# --- Process Documents Button ---
process_button = tk.Button(root, text="Process Documents", command=process_documents)
process_button.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

# --- Status Label ---
status_label = tk.Label(root, text="Ready")
status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# --- Search Bar ---
search_label = tk.Label(root, text="Search:")
search_label.grid(row=3, column=0, padx=5, pady=5)

search_entry = tk.Text(root, height=2, width=50)
search_entry.grid(row=3, column=1, padx=5, pady=5)

search_button = tk.Button(root, text="Search", command=search_documents)
search_button.grid(row=3, column=2, padx=5, pady=5)

# --- Search Results ---
search_results_label = tk.Label(root, text="Search Results:")
search_results_label.grid(row=4, column=0, padx=5, pady=5)

search_results = tk.Text(root, wrap=tk.WORD, height=10, width=70)
search_results.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# --- Run the UI ---
root.mainloop()
