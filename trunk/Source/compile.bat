set winisondir=%CD%
CD ..
set outdir=%CD%

C:
CD python25
CD pyinstaller

C:\python25\python.exe Configure.py

C:\python25\python.exe Makespec.py --onefile --windowed --out=%outdir% %winisondir%\winison.pyw

C:\python25\python.exe Build.py %outdir%\winison.spec

pause