# This file automagically generated by packman
[Setup]

AppID=${APPID}
AppName=${NAME}
AppVersion=${VERSION}
AppPublisher=${ORGANIZATION}
AppPublisherURL=${WEBSITE}
AppSupportURL=${WEBSITE}
AppUpdatesURL=${WEBSITE}
DefaultDirName={pf}\\${NAME}
DefaultGroupName=${NAME}
OutputDir=${OUTDIR}
OutputBaseFilename=${PACKAGENAME}
Compression=lzma/Max
SolidCompression=true
AlwaysShowDirOnReadyPage=true
UserInfoPage=no
UsePreviousUserInfo=no
DisableDirPage=yes
DisableProgramGroupPage=yes
DisableReadyPage=no
WizardImageFile="${GRAPHICSPATH}/win-banner.bmp"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "${OUTDIR}/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\${NAME}"; Filename: "{app}\\${SHORTNAME}.exe" ; IconFilename: "{app}\win.ico";
Name: "{group}\{cm:UninstallProgram,{NAME}}"; Filename: "{uninstallexe}";
Name: "{commondesktop}\\${NAME}"; Filename: "{app}\\${SHORTNAME}.exe"; IconFilename: "{app}\win.ico";
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\\${NAME}"; Filename: "{app}\\${SHORTNAME}.exe"; IconFilename: "{app}\win.ico";

[Run]
Filename: {app}\\${SHORTNAME}.exe; Description: "{cm:LaunchProgram,${NAME}}"; Flags: skipifsilent NoWait PostInstall; 
