set winisondir=%CD%
CD ..
set outdir=%CD%

C:
CD python25
CD pyinstaller

C:\python25\python.exe Configure.py

C:\python25\python.exe Makespec.py --onedir --windowed --out=%outdir% %winisondir%\winison.py

C:\python25\python.exe Build.py %outdir%\winison.spec

copy %winisondir%\*.py %outdir%\dist\winison
copy %winisondir%\Licence.txt %outdir%\dist\winison
copy %winisondir%\my_version_of_unison %outdir%\dist\winison

pause