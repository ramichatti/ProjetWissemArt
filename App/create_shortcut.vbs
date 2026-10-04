Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\WissemArt Achat.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = WScript.ScriptFullName & "\..\WissemArt_Achat.bat"
oLink.WorkingDirectory = WScript.ScriptFullName & "\.."
oLink.Description = "WissemArt Achat - Gestion Professionnelle"
oLink.IconLocation = WScript.ScriptFullName & "\..\LogoWissem.ico"
oLink.Save
WScript.Echo "Raccourci cree sur le bureau avec succes!"
