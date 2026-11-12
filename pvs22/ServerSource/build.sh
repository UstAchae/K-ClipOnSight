#!/bin/sh
# Builds the server side from PVS22Mod.cs: the public mod (CLIPON_ALL: AN/PVS-27, AN/PVS-30, UTC XII) into
# bin/Release/all/, and the author's private AN/PVS-22 (CLIPON_PVS22) into bin/Release/pvs22/.
cd "$(dirname "$0")"
DOTNET=D:/vssm-work/tools/dotnet/dotnet.exe
"$DOTNET" build -c Release -nologo -v q -p:AssemblyName=UstAchae.ClipOnSight -p:DefineConstants=CLIPON_ALL \
  -p:IntermediateOutputPath=obj/all/ -o bin/Release/all || exit 1
"$DOTNET" build -c Release -nologo -v q -p:AssemblyName=UstAchae.ClipOnSight.PVS22 -p:DefineConstants=CLIPON_PVS22 \
  -p:IntermediateOutputPath=obj/pvs22/ -o bin/Release/pvs22 || exit 1
