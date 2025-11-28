@echo off
echo zamn... Reverting batch file

assoc .kl=
ftype KeylangFile=
reg delete "HKCR\KeylangFile" /f

echo Keylang associations removed.
pause
