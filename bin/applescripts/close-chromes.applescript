-- tell application "Finder" to close every window
-- tell application "Google Chrome" to close every window
-- tell application "Google Chrome" to quit

-- START GENAI@CHATGPT4
tell application "System Events"
	set chromeProcesses to every process whose name is "Google Chrome"
	repeat with aProcess in chromeProcesses
		tell application "Google Chrome" to quit
		delay 1
	end repeat
end tell
-- END GENAI@CHATGPT4