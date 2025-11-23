# Export all Watson Orchestrate agents
# Run from: cd 'D:\Python\HireIT AI'; .\venv\Scripts\Activate.ps1; .\export-agents.ps1

Write-Host "Exporting all Watson Orchestrate agents..." -ForegroundColor Cyan

$agents = "jira_issue_management_agent_c6f462e3","Mass_Review_7330tb","Job_Listing_Briefing_Agent","gmail_email_agent_2fc29846","gmail_client_outreach_5da0af2a","Email_Blast_9071T9","Transcriber_0057hm","SheetManager","Interviewer_5060SD","Text_Parser","google_drive_file_management_agent_08760319","google_drive_folder_management_agent_201ce6ae","DataHub","Reviewer_Agent_2909kd","Hello_World_Agent","Job_Listing_4857jv","Applicant_Tracker_0642Mt","AskOrchestrate"

$successCount = 0
$failCount = 0

foreach ($name in $agents) {
    $outputFile = "agents/$name.yaml"
    Write-Host "Exporting $name..." -ForegroundColor Yellow
    
    orchestrate agents export --name $name --kind native --output $outputFile --agent-only
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Success: $outputFile" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "Failed: $name" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "Summary: $successCount success, $failCount failed" -ForegroundColor Cyan
