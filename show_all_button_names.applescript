on run
	tell application "System Events"
		if not (exists process "ChatGPT") then
			display dialog "ChatGPT 프로세스를 찾을 수 없습니다."
			return
		end if
		tell process "ChatGPT"
			if not (exists window 1) then
				display dialog "ChatGPT 창이 없습니다."
				return
			end if
			set allElements to entire contents of window 1
			set buttonInfos to {}
			repeat with elem in allElements
				try
					if class of elem is button then
						set btnHelp to ""
						set btnValue to ""
						set btnDesc to ""
						try
							set btnHelp to help of elem
						end try
						try
							set btnValue to value of elem
						end try
						try
							set btnDesc to description of elem
						end try
						set info to "Help: " & btnHelp & " | Value: " & btnValue & " | Desc: " & btnDesc
						set end of buttonInfos to info
					end if
				end try
			end repeat
			set allInfo to ""
			repeat with info in buttonInfos
				set allInfo to allInfo & info & linefeed
			end repeat
			display dialog allInfo buttons {"확인"} default button 1
		end tell
	end tell
end run
