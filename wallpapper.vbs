dim shell, user

Set shell = WScript.CreateObject("WScript.Shell")
Set user = shell.ExpandEnvironmentStrings("%USER%")

Set fso = CreateObject("Scripting.FileSystemObject")

windowsDir = fso.GetSpecialFolder(0) 
wallpaper = "D:\wallpaper\wp4354823.jpg"

shell.RegWrite "HKCU\Control Panel\Desktop\Wallpaper", wallpaper

shell.Run "%windowsDir%\System32\RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters", 1, True