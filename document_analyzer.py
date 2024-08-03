import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# Load environment variables from .env file
load_dotenv()

def get_pdf_page_count(file):
        parser = PDFParser(file)
        document = PDFDocument(parser)
        return len(document.catalog['Pages'].resolve()['Kids'])

def analyze_document(file):
    endpoint = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
    key = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")

    if not endpoint or not key:
        raise ValueError("DOCUMENTINTELLIGENCE_ENDPOINT and DOCUMENTINTELLIGENCE_API_KEY must be set in the .env file")

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    file_content = file.read()

    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        file_content,
        content_type="application/octet-stream",
        output_content_format=ContentFormat.MARKDOWN,
    )

    result = poller.result()
    return result.content