# Destination folder
$exportPath = "C:\Users\AM3\x\SentItems"

# Create folder if needed
if (!(Test-Path $exportPath)) {
    New-Item -ItemType Directory -Path $exportPath | Out-Null
}

# Start Outlook COM object
$outlook = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace("MAPI")

# Get default Sent Items folder
$sentFolder = $namespace.GetDefaultFolder(
    [Microsoft.Office.Interop.Outlook.OlDefaultFolders]::olFolderSentMail
)

# Counter
$count = 0

foreach ($mail in $sentFolder.Items) {

    # Only process mail items
    if ($mail -is [__ComObject]) {

        try {

            # Build safe filename
            $subject = $mail.Subject

            if ([string]::IsNullOrWhiteSpace($subject)) {
                $subject = "No Subject"
            }

            # Remove invalid filename chars
            $subject = $subject -replace '[\\/:*?"<>|]', '_'

            # Trim length
            if ($subject.Length -gt 80) {
                $subject = $subject.Substring(0,80)
            }

            $date = $mail.SentOn.ToString("yyyy-MM-dd_HH-mm-ss")

            $filename = "$date - $subject.msg"

            $fullPath = Join-Path $exportPath $filename

            # Avoid duplicates
            $i = 1
            while (Test-Path $fullPath) {
                $fullPath = Join-Path $exportPath "$date - $subject ($i).msg"
                $i++
            }

            # Save as MSG
            $mail.SaveAs($fullPath, 3)

            $count++
            Write-Host "Saved: $filename"

        } catch {
            Write-Host "Error processing item"
        }
    }
}

Write-Host ""
Write-Host "Done. Exported $count messages."

