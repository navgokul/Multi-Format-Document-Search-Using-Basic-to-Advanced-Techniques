# Document Search Engine: Architecture, Design, and Implementation

This document outlines the architecture, design choices, and implementation details for a simple document search engine built using Python.

## 1. Architecture and Design

The search engine follows a modular design, separating the core functionalities into distinct components:

### 1.1. Data Ingestion and Processing:

- **Document Loader:** This module handles loading various document types (PDF, images, text files) from a specified directory. It extracts text content and basic metadata (filename, size, creation date) from each document.
- **Text Extraction:** Utilizes libraries like PyMuPDF (for PDFs), Pillow (for images), and pytesseract (OCR for images) to extract text content.

### 1.2. Indexing:

- **Whoosh Indexer:** Employs the Whoosh library to create and manage a full-text search index.
- **Schema Definition:** Defines the structure of the index, including fields for filename, size, creation date, and the indexed content.
- **Stemming Analyzer:** Uses a stemming analyzer to improve search accuracy by reducing words to their root form.

### 1.3. Search and Retrieval:

- **Whoosh Searcher:** Opens the created index and allows querying using the Whoosh query language.
- **Result Ranking:** Whoosh handles basic relevance ranking based on term frequency and other factors.

### 1.4. User Interface (GUI):

- **Tkinter-based GUI:** Provides a simple interface for:
- Selecting the source directory containing documents.
- Selecting the destination directory for copied files.
- Triggering the indexing process.
- Entering search queries.
- Displaying search results (currently limited to filenames).

### 1.5. File Management:

- **shutil:** Used for copying files from the source to the destination directory based on search results.

## 2. Approach and Design Choices

- **Modular Design:** Promotes code organization, maintainability, and potential for future expansion (e.g., adding support for more document types or implementing advanced ranking algorithms).
- **Whoosh Library:** Chosen for its ease of use, Python integration, and sufficient features for a basic search engine.
- **Stemming:** Improves search recall by handling different word forms.
- **Tkinter:** Provides a straightforward way to create a basic GUI for user interaction.

## 3. Skills and Tools Required

- **Programming Language:** Python 3.x
- **Libraries:**
- PyMuPDF (fitz): For PDF processing.
- Pillow (PIL): For image handling.
- pytesseract: For Optical Character Recognition (OCR).
- Whoosh: For indexing and searching.
- Tkinter: For the graphical user interface.
- shutil: For file operations.
- tqdm: For progress bars.
- **Tools:**
- Text editor or IDE (e.g., VS Code, PyCharm).
- Tesseract OCR engine (needs to be installed separately).

## 4. Implementation Steps and Challenges

### 4.1. Steps:

1. **Set up Environment:** Install required Python libraries.
2. **Implement Data Ingestion:** Write functions to load and extract text from different document types.
3. **Implement Indexing:** Create the Whoosh index schema and indexing logic.
4. **Implement Search:** Write functions to query the index and retrieve results.
5. **Build GUI:** Design and implement the user interface using Tkinter.
6. **Integrate Components:** Connect the GUI to the indexing, searching, and file copying functionalities.
7. **Testing and Refinement:** Thoroughly test the application with various documents and search queries.

### 4.2. Challenges:

- **Error Handling:** Robust error handling is crucial, especially during document loading and text extraction, as different file formats and encodings can cause issues.
- **OCR Accuracy:** OCR using pytesseract might not always be perfectly accurate, especially for complex images or handwritten text.
- **Search Relevance:** The current implementation uses basic ranking provided by Whoosh. Implementing more sophisticated ranking algorithms would significantly improve search accuracy.
- **GUI Design:** The current GUI is very basic. A more user-friendly interface with features like result display, filtering, and sorting would enhance the user experience.

## 5. Future Improvements

- **Enhanced Search:** Implement more advanced ranking algorithms (e.g., TF-IDF, BM25) to improve search result relevance.
- **Support for More File Types:** Add support for other document formats like Microsoft Word (.docx), Excel (.xlsx), etc.
- **Improved GUI:** Create a more user-friendly interface with better result display, filtering options, and potentially document previews.
- **Metadata Integration:** Utilize extracted metadata for faceting and filtering search results.
- **Error Logging:** Implement proper logging to record errors encountered during processing for debugging and improvement.
