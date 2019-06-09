Set args = WScript.Arguments.Unnamed
Set objShell = CreateObject("WScript.Shell")
objDesktop = objShell.SpecialFolders("Desktop")
Set objLink = objShell.CreateShortcut(objDesktop & "\teste.lnk")

objLink.TargetPath = args.item(0) & "PDFConverter.exe"
objLink.WindowStyle = 3
objLink.Save

WScript.Quit