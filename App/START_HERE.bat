@echo off
title WissemArt Achat - Installation
color 1F
cls
echo.
echo ╔════════════════════════════════════════════════╗
echo ║        WissemArt Achat - Installation         ║
echo ╚════════════════════════════════════════════════╝
echo.
echo  Tous les fichiers sont prets !
echo  Icone : LogoWissem.ico
echo.
echo  [1] Creer un raccourci sur le BUREAU (avec icone)
echo  [2] Lancer l'application maintenant
echo  [3] Quitter
echo.
set /p choice="  Votre choix (1, 2 ou 3) : "

if "%choice%"=="1" goto CREATE_SHORTCUT
if "%choice%"=="2" goto LAUNCH_APP
if "%choice%"=="3" goto END

:CREATE_SHORTCUT
cls
echo.
echo  Creation du raccourci sur le bureau...
cscript //nologo create_shortcut.vbs
echo.
echo  Voulez-vous lancer l'application maintenant? (O/N)
set /p launch="  Votre choix : "
if /i "%launch%"=="O" goto LAUNCH_APP
goto END

:LAUNCH_APP
cls
echo.
echo  Lancement de WissemArt Achat...
echo.
python AppAchat.py
goto END

:END
echo.
echo  Au revoir !
timeout /t 2 >nul
exit
