set winisondir=%CD%
CD ..
set outdir=%CD%

C:
CD python25
CD pyinstaller

C:\python25\python.exe Configure.py

C:\python25\python.exe Makespec.py --onefile --windowed --out=%outdir% %winisondir%\winison.py

C:\python25\python.exe Build.py %outdir%\winison.spec

copy %winisondir%\*.py %outdir%\dist

pause