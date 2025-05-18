@echo off
REM Sjekk at .git-mappe finnes
if not exist ".git" (
    echo Du maa kjoere dette fra rotmappa til et git-repo!
    exit /b 1
)
REM Lag commit-msg-hook
(
echo @echo off
echo echo.
echo echo [GL!TCH] Commit-initiativ detektert. Reality Integrity: UNSTABLE.
echo echo %%date%% %%time%%: Commit message review in progress...
echo echo.
) > .git\hooks\commit-msg

REM Sett riktig attributt (valgfritt, mest for syns skyld)
attrib +x .git\hooks\commit-msg

echo Ferdig! Glitchy noir commit-msg hook er aktiv i dette repoet.
echo Proev aa committe noe for aa se effekten.
pause