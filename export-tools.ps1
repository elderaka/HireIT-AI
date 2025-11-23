# Export all Watson Orchestrate tools to /tools-export folder

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# List of all tools from orchestrate tools list
$tools = @(
    "download_public_bytes",
    "send_an_email_158dc",
    "sniff_html_interstitial",
    "send_an_email_f7072",
    "extract_drive_file_id",
    "get_files_ee629",
    "parse_csv_bytes",
    "parse_file_bytes",
    "parse_drive_public_link",
    "Untitled_2_3628Jf",
    "get_file_content_google_drive_9ac1c",
    "get_file_content_google_drive_f56c6",
    "create_object_8399b",
    "build_text_bytes",
    "upload_file_google_drive_9e28c",
    "Untitled_4334HO",
    "debug_head_bytes",
    "get_file_content_google_drive_08740",
    "get_files_935b4",
    "get_folders_598ac",
    "get_revisions_3f651",
    "i__get_flow_status_intrinsic_tool__",
    "build_file_bytes",
    "Untitled_3_8645CG",
    "make_drive_download_link",
    "build_csv_bytes",
    "Untitled_1_8945yC",
    "job_listing_to_rows",
    "job_listing_schema",
    "gmail_send_email_8def1",
    "fetch_audio_from_url",
    "validate_job_listing_json",
    "sniff_table_file_type",
    "apply_sheet_patch",
    "generateFile",
    "transcribe_job_interview",
    "upload_file_google_drive_615a2",
    "parse_xlsx_bytes",
    "gmail_send_email_e309b",
    "create_a_folder_google_drive_aafe9",
    "get_folder_items_1c197",
    "get_folders_979f4",
    "get_file_content_google_drive_628ec",
    "upload_file_google_drive_07b66",
    "get_files_e0148",
    "get_folders_fd89f",
    "get_revisions_e304e",
    "recognizeAudio",
    "send_an_email_31e83",
    "extract_drive_folder_id",
    "Untitled_4_7989NK",
    "decode_b64_to_bytes",
    "make_sheets_export_link",
    "normalize_job_intake",
    "make_job_listing_json",
    "parse_sheet_public",
    "template_headers_from_xlsx",
    "delete_an_email_35909",
    "send_an_email_5ecff",
    "list_emails_0396a",
    "delete_an_email_c37f9",
    "send_an_email_510d2",
    "list_emails_71f10",
    "build_csv",
    "get_file_content_google_drive_c1ff5",
    "Untitled_5_4747FC",
    "delete_an_email_3e137",
    "send_an_email_0f139",
    "list_emails_9a542",
    "build_json_bytes",
    "gmail_send_email_78bc0",
    "get_issue_priorities_a6767",
    "get_public_text_or_json",
    "create_an_issue_e6459",
    "get_issues_26da8",
    "delete_an_issue_3eaab",
    "get_project_issue_types_ff606",
    "get_users_8596c",
    "update_an_issue_d1129",
    "get_projects_6c386",
    "get_users_a026d",
    "get_users_096e5",
    "get_folders_d38e5",
    "upload_file_google_drive_66354",
    "upload_file_google_drive_7e37e"
)

# Create tools-export directory if it doesn't exist
$exportDir = "tools-export"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir | Out-Null
}

$total = $tools.Count
$current = 0

Write-Host "Starting export of $total tools to $exportDir folder..."

foreach ($tool in $tools) {
    $current++
    $outputFile = "$exportDir\$tool.zip"
    
    Write-Host "[$current/$total] Exporting: $tool"
    
    orchestrate tools export --name $tool --output $outputFile 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Success" -ForegroundColor Green
    } else {
        Write-Host "  Failed" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Export completed! Check the $exportDir folder"
