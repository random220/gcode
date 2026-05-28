# =========================================================
# Export Outlook Sent Items recipient details to CSV
# Includes:
#   - From
#   - To
#   - CC
#   - BCC
#   - Subject
#   - Sent Date
#
# Output format:
#   "Display Name" <email@domain.com>
#
# =========================================================

# Output CSV path
$outputCsv = "C:\Users\AM3\x\sent_addresses.csv"

# Ensure output folder exists
$outputDir = Split-Path $outputCsv

if (!(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Start Outlook COM
$outlook = New-Object -ComObject Outlook.Application
$namespace = $outlook.GetNamespace("MAPI")

# Sent Items folder
# 5 = olFolderSentMail
$sentFolder = $namespace.GetDefaultFolder(5)

# Get items and sort newest first
$items = $sentFolder.Items
$items.Sort("[SentOn]", $true)

# Result array
$results = @()

# =========================================================
# Resolve recipient to:
#   "Display Name" <smtp@domain.com>
# =========================================================

function Get-RecipientString($recipient) {

    try {

        if ($recipient -eq $null) {
            return ""
        }

        $displayName = $recipient.Name
        $smtp = $null

        # Try Exchange resolution
        try {

            if ($recipient.AddressEntry -ne $null) {

                $addressEntry = $recipient.AddressEntry

                if ($addressEntry.Type -eq "EX") {

                    $exchangeUser = $addressEntry.GetExchangeUser()

                    if ($exchangeUser -ne $null) {
                        $smtp = $exchangeUser.PrimarySmtpAddress
                    }

                }

            }

        } catch {
        }

        # Fallback
        if ([string]::IsNullOrWhiteSpace($smtp)) {
            $smtp = $recipient.Address
        }

        # Final fallback
        if ([string]::IsNullOrWhiteSpace($smtp)) {
            $smtp = "UNKNOWN"
        }

        # Escape quotes
        $displayName = $displayName -replace '"', "'"

        return "`"$displayName`" <$smtp>"

    } catch {

        return "<UNRESOLVED>"

    }
}

# =========================================================
# Process messages
# =========================================================

$total = $items.Count

Write-Host ""
Write-Host "Processing $total Outlook Sent Items..."
Write-Host ""

for ($i = 1; $i -le $total; $i++) {

    try {

        $mail = $items.Item($i)

        # Skip nulls
        if ($mail -eq $null) {
            continue
        }

        # Only MailItem objects
        # 43 = olMail
        if ($mail.Class -ne 43) {
            continue
        }

        # Skip mails with no recipients
        if ($mail.Recipients.Count -eq 0) {
            continue
        }

        $toAddresses  = @()
        $ccAddresses  = @()
        $bccAddresses = @()

        # Process recipients
        foreach ($recipient in $mail.Recipients) {

            try {

                $formatted = Get-RecipientString $recipient

                switch ($recipient.Type) {

                    1 { $toAddresses  += $formatted }   # To
                    2 { $ccAddresses  += $formatted }   # CC
                    3 { $bccAddresses += $formatted }   # BCC
                }

            } catch {
            }
        }

        # From address
        $fromAddress = $mail.SenderEmailAddress

        if ([string]::IsNullOrWhiteSpace($fromAddress)) {
            $fromAddress = "UNKNOWN"
        }

        # Add result
        $results += [PSCustomObject]@{

            SentOn = $mail.SentOn

            From = $fromAddress

            To = ($toAddresses -join "; ")

            CC = ($ccAddresses -join "; ")

            BCC = ($bccAddresses -join "; ")

            Subject = $mail.Subject
        }

        # Progress
        if (($i % 100) -eq 0) {

            Write-Host ("Processed {0} / {1}" -f $i, $total)

        }

    } catch {

        # Soft-fail only
        Write-Host ("Skipping problematic item {0}" -f $i)

    }
}

# =========================================================
# Export CSV
# =========================================================

$results |
    Export-Csv `
        -Path $outputCsv `
        -NoTypeInformation `
        -Encoding UTF8

Write-Host ""
Write-Host "==============================================="
Write-Host "DONE"
Write-Host "==============================================="
Write-Host ""
Write-Host "CSV exported to:"
Write-Host $outputCsv
Write-Host ""
Write-Host ("Exported {0} messages." -f $results.Count)
Write-Host ""
