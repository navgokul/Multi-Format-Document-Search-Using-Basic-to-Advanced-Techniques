# Document Search Engine with Senatnce Transformers 

## Overall Design

This document search engine allows users to index and search through a collection of documents in various formats. The system employs a combination of natural language processing (NLP) and information retrieval techniques to provide accurate and efficient search results.

## Key Features

- **Document Ingestion:** Loads documents from a specified directory, supporting:
- PDFs
- Images (JPEG, PNG, etc.)
- Text files (TXT)
- **Text Extraction:** Extracts text content from different document formats using:
- **PyMuPDF:** For extracting text from PDF files.
- **Pillow and Pytesseract:** For extracting text from images using Optical Character Recognition (OCR).
- **Python Standard Library:** For directly reading text from text files.
- **Text Embedding:** Converts extracted text into numerical representations (embeddings) using:
- **Sentence-Transformers:** Leverages pre-trained language models for generating semantically meaningful embeddings.
- **Indexing:** Creates a searchable index of the document embeddings using:
- **FAISS:** An efficient and scalable library for similarity search in high-dimensional spaces.
- **Search:** Provides a search function that:
- Queries the FAISS index using user-provided search terms.
- Retrieves documents based on the similarity between the search query embedding and the document embeddings.

## Tools and Techniques

- **PyMuPDF:** A Python library for working with PDF files, used for text extraction.
- **Pillow:** A Python Imaging Library (PIL) fork for image processing.
- **Pytesseract:** A Python wrapper for Google's Tesseract OCR engine.
- **Sentence-Transformers:** A Python framework for sentence and text embeddings using transformer models.
- **FAISS:** Facebook AI Similarity Search - a library for efficient similarity search.
- **Python Standard Library:** Used for file handling, metadata extraction, and other core functionalities.

## Future Enhancements

- **Support for More Document Formats:** Extend support to include Microsoft Word documents (.docx), HTML files, and other common formats.
- **Improved Text Extraction Accuracy:** Explore more advanced OCR techniques and PDF parsing libraries to enhance text extraction accuracy, especially for complex layouts and scanned documents.
- **User Interface:** Develop a user-friendly interface (web or desktop-based) for:
- Uploading documents.
- Initiating searches.
- Displaying search results in an organized and informative manner.
- **Advanced Search Features:** Implement advanced search capabilities such as:
- **Boolean Queries:** Allow users to combine search terms using operators like AND, OR, and NOT.
- **Fuzzy Search:** Enable searching for documents containing terms similar to the search query, accounting for typos or variations in spelling.
- **Field-Specific Search:** Allow users to restrict their search to specific fields within the documents (e.g., title, author, keywords).
- **Testing and Optimization:** Conduct thorough testing with a large corpus of documents to evaluate performance and optimize:
- Indexing speed.
- Search response time.
- Resource utilization (memory and CPU).

## Conclusion

This document search engine provides a robust and efficient solution for indexing and searching through collections of multi-format documents. By leveraging the power of LLMs and deep learning techniques for text embedding and similarity search, the system enables users to quickly and accurately find the information they need. The planned enhancements will further improve the system's functionality, usability, and performance.
```
