# Document Search Application Documentation

This document provides detailed information on the setup, functionality, and usage of the Document Search Application. This application processes documents, extracts text, generates embeddings, and indexes them using Pinecone. It provides a user-friendly interface to search and retrieve documents based on query embeddings.

## Table of Contents
1. [Introduction](#introduction)
2. [Configuration](#configuration)
3. [Global Variables](#global-variables)
4. [UI Functions](#ui-functions)
5. [Document Loading Functions](#document-loading-functions)
6. [Pinecone Index Management](#pinecone-index-management)
7. [Search Functionality](#search-functionality)
8. [UI Setup](#ui-setup)
9. [Running the Application](#running-the-application)

## Introduction

The Document Search Application is designed to process various document formats, extract textual data, generate embeddings using a language model, and index them using Pinecone. Users can search through indexed documents using a graphical user interface built with Tkinter.

## Configuration

Before running the application, ensure you configure the following settings in the script:

```python
PINECONE_API_KEY = 'your-pinecone-api-key'  # Replace with your Pinecone API key
PINECONE_ENVIRONMENT = 'your-pinecone-environment'  # Replace with your Pinecone environment
INDEX_NAME = 'document-index'
DEFAULT_LLM_MODEL = 'all-MiniLM-L6-v2'
```

## Global Variables

### Index and Model

- `index`: Holds the Pinecone index instance.
- `model`: Holds the instance of the SentenceTransformer model.

## UI Functions

### `select_document_directory()`

Opens a directory selection dialog and updates the directory path in the UI.

### `update_status(message)`

Updates the status label in the UI with the given message.

### `process_documents()`

Starts a separate thread to load, process, and index documents from the selected directory.

### `search_documents()`

Searches the indexed documents based on the user's query and displays the results in the UI.

### `select_llm_model(model_name: str)`

Allows selecting a different language model for embedding generation (feature not fully implemented in UI).

## Document Loading Functions

### `load_documents(directory: str) -> List[Dict]`

Loads documents from the specified directory and processes each file type accordingly. Supports PDF, image, and text files.

### `load_pdf(filepath: str) -> Dict`

Processes a PDF file and generates its embedding.

### `load_image(filepath: str) -> Dict`

Processes an image file and extracts text using OCR (pytesseract), then generates its embedding.

### `load_text_file(filepath: str) -> Dict`

Processes a text file and generates its embedding.

### `get_metadata(filepath: str) -> Dict`

Extracts metadata (filename, size, creation date) from a file.

## Pinecone Index Management

### `initialize_pinecone()`

Initializes the Pinecone connection and creates the index if it does not exist.

### `create_index(index: Index, documents: List[Dict])`

Creates or updates the Pinecone index with document embeddings.

## Search Functionality

### `search_index(index, query_str: str, top_k: int = 5)`

Searches the Pinecone index based on the query embedding and updates the search results text area.

## UI Setup

The UI is built using Tkinter. It includes components for selecting the document directory, processing documents, entering search queries, and displaying search results.

### Main Components

- **Document Directory Selection**: Allows users to select the directory containing documents to be processed.
- **Process Documents Button**: Triggers the document processing and indexing.
- **Status Label**: Displays the current status of the application.
- **Search Bar**: Allows users to enter queries to search through indexed documents.
- **Search Results**: Displays the search results based on the query.

## Running the Application

To run the application, execute the script in a Python environment with the required libraries installed. Ensure you have the correct Pinecone API key and environment configured.

```bash
python document_search_app.py
```

The application window will open, allowing you to select a document directory, process documents, and perform search queries. The status label and search results area will update accordingly.

This completes the documentation for the Document Search Application. For any further customization or enhancements, refer to the respective sections in the script.
