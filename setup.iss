[Setup]
AppName=EZBoot
AppVersion=1.1
DefaultDirName={autopf}\EZBoot
DefaultGroupName=EZBoot
OutputDir=.
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
OutputManifestFile=True

[Files]
Source: "C:\Users\David\Desktop\Script\dist\EZBoot.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Script\create_task.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\create_task.ps1"""; Flags: runhidden waituntilterminated; Description: "Create scheduled task"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    Exec('powershell.exe', '-ExecutionPolicy Bypass -File "{app}\create_task.ps1"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    
  end;
end;
