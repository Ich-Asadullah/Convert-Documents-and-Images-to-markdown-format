# Document Analyzer

A Streamlit-based web application that uses Azure's Document Intelligence service to analyze documents and images, outputting the results in Markdown format.

## Features

- Secure login system
- File upload for PDF and image files (jpg, jpeg, png)
- Document analysis using Azure Document Intelligence
- Results displayed in Markdown format

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- An Azure account with Document Intelligence service set up
- Azure Document Intelligence endpoint and API key

## Installation

1. Clone this repository:
git clone https://github.com/your-username/document-analyzer.git
cd document-analyzer
Copy
2. Install the required packages:
pip install -r requirements.txt
Copy
3. Create a `.env` file in the root directory with your Azure credentials:
DOCUMENTINTELLIGENCE_ENDPOINT=your_endpoint_here
DOCUMENTINTELLIGENCE_API_KEY=your_api_key_here
Copy
## Usage

1. Run the Streamlit app:
streamlit run app.py
Copy
2. Open your web browser and go to `http://localhost:8501`

3. Log in using the default credentials:
- Username: admin
- Password: admin

4. Upload a PDF or image file and click "Analyze Document" to see the results.

## File Structure

- `app.py`: Main Streamlit application
- `document_analyzer.py`: Module for document analysis using Azure Document Intelligence
- `requirements.txt`: List of required Python packages
- `.env`: Environment variables file (not included in repository)

## Contributing

Contributions to the Document Analyzer project are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Azure Document Intelligence](https://azure.microsoft.com/en-us/services/cognitive-services/document-intelligence/)
