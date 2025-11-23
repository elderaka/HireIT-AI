# Export all Watson Orchestrate agents to the agents folder
# Requires: Python venv activated with orchestrate CLI installed

Write-Host "Exporting all Watson Orchestrate agents..." -ForegroundColor Cyan

# Define agent names (extracted from orchestrate agents list)
$agents = @(
    @{name="jira_issue_management_agent_c6f462e3"; displayName="Issue Manager"},
    @{name="Mass_Review_7330tb"; displayName="Mass Review"},
    @{name="Job_Listing_Briefing_Agent"; displayName="Job Listing Briefing"},
    @{name="gmail_email_agent_2fc29846"; displayName="Email management"},
    @{name="gmail_client_outreach_5da0af2a"; displayName="Client Outreach on Gmail"},
    @{name="Email_Blast_9071T9"; displayName="Email Blast"},
    @{name="Transcriber_0057hm"; displayName="Transcriber"},
    @{name="SheetManager"; displayName="Sheet Manager"},
    @{name="Interviewer_5060SD"; displayName="Interviewer"},
    @{name="Text_Parser"; displayName="Text Parser"},
    @{name="google_drive_file_management_agent_08760319"; displayName="File management"},
    @{name="google_drive_folder_management_agent_201ce6ae"; displayName="Folder management"},
    @{name="DataHub"; displayName="DataHub"},
    @{name="Reviewer_Agent_2909kd"; displayName="Reviewer"},
    @{name="Hello_World_Agent"; displayName="Hello World Agent"},
    @{name="Job_Listing_4857jv"; displayName="Job Listing"},
    @{name="Applicant_Tracker_0642Mt"; displayName="Applicant Tracker"},
    @{name="AskOrchestrate"; displayName="AskOrchestrate"}
)

# Create agents directory if it doesn't exist
$agentsDir = "agents"
if (-not (Test-Path $agentsDir)) {
    New-Item -ItemType Directory -Path $agentsDir | Out-Null
}

# Export each agent
$successCount = 0
$failCount = 0

foreach ($agent in $agents) {
    $name = $agent.name
    $display = $agent.displayName
    $outputFile = "$agentsDir/$name.yaml"
    
    Write-Host "`nExporting '$display' ($name)..." -ForegroundColor Yellow
    
    try {
        # Run the orchestrate export command
        $command = "orchestrate agents export --name $name --kind native --output $outputFile --agent-only"
        Invoke-Expression $command
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "âœ“ Successfully exported to $outputFile" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "âœ— Failed to export $name (exit code: $LASTEXITCODE)" -ForegroundColor Red
            $failCount++
        }
    }
    catch {
        Write-Host "âœ— Error exporting $name : $_" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Export Summary:" -ForegroundColor Cyan
Write-Host "  Success: $successCount" -ForegroundColor Green
Write-Host "  Failed:  $failCount" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
