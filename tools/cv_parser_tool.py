"""Tool to extract and parse CVs from a Google Drive folder.

This tool helps the Reviewer Agent get CV content from Drive.
"""

import os
from typing import Dict, List
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
import io
import PyPDF2


def get_drive_service():
    """Initialize Google Drive service with credentials."""
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    # Try to get credentials from environment or file
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials.json')
    
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Google credentials not found at {creds_path}")
    
    credentials = service_account.Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    
    return build('drive', 'v3', credentials=credentials)


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        return f"[Error extracting text: {str(e)}]"


def parse_cvs_from_folder(folder_id: str, candidate_name: str = None) -> Dict:
    """Parse CV files from a Google Drive folder.
    
    Parameters
    ----------
    folder_id : str
        The Google Drive folder ID containing CV files
    candidate_name : str, optional
        If provided, only parse CVs matching this name
    
    Returns
    -------
    Dict
        {
            "cvs": [
                {
                    "file_name": str,
                    "candidate_name": str (extracted from filename),
                    "cv_text": str,
                    "file_id": str
                }
            ],
            "total_found": int,
            "errors": List[str]
        }
    """
    try:
        service = get_drive_service()
        
        # Query for PDF files in the folder
        query = f"'{folder_id}' in parents and (mimeType='application/pdf' or name contains '.pdf') and trashed=false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name, mimeType)",
            pageSize=100
        ).execute()
        
        files = results.get('files', [])
        
        cvs = []
        errors = []
        
        for file in files:
            file_name = file['name']
            file_id = file['id']
            
            # Extract candidate name from filename (remove .pdf and clean up)
            extracted_name = file_name.replace('.pdf', '').replace('_', ' ').strip()
            
            # Filter by candidate name if provided
            if candidate_name and candidate_name.lower() not in extracted_name.lower():
                continue
            
            try:
                # Download file content
                request = service.files().get_media(fileId=file_id)
                file_buffer = io.BytesIO()
                downloader = MediaIoBaseDownload(file_buffer, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                # Extract text
                pdf_bytes = file_buffer.getvalue()
                cv_text = extract_text_from_pdf_bytes(pdf_bytes)
                
                cvs.append({
                    "file_name": file_name,
                    "candidate_name": extracted_name,
                    "cv_text": cv_text,
                    "file_id": file_id
                })
                
            except Exception as e:
                errors.append(f"Failed to parse {file_name}: {str(e)}")
        
        return {
            "cvs": cvs,
            "total_found": len(cvs),
            "errors": errors
        }
        
    except Exception as e:
        return {
            "cvs": [],
            "total_found": 0,
            "errors": [f"Failed to access folder: {str(e)}"]
        }


def get_job_listing_from_folder(folder_id: str) -> Dict:
    """Get job listing content from a folder.
    
    Looks for job-listing.txt or job_intake.json in the folder.
    
    Parameters
    ----------
    folder_id : str
        The Google Drive folder ID
    
    Returns
    -------
    Dict
        {
            "job_listing": str (content),
            "file_name": str,
            "found": bool
        }
    """
    try:
        service = get_drive_service()
        
        # Look for job listing files
        query = f"'{folder_id}' in parents and (name='job-listing.txt' or name='job_intake.json') and trashed=false"
        
        results = service.files().list(
            q=query,
            fields="files(id, name)",
            orderBy="modifiedTime desc",
            pageSize=1
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            return {
                "job_listing": "",
                "file_name": "",
                "found": False
            }
        
        file = files[0]
        
        # Download content
        request = service.files().get_media(fileId=file['id'])
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        content = file_buffer.getvalue().decode('utf-8')
        
        return {
            "job_listing": content,
            "file_name": file['name'],
            "found": True
        }
        
    except Exception as e:
        return {
            "job_listing": "",
            "file_name": "",
            "found": False,
            "error": str(e)
        }
