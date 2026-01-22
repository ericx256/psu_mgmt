for /f %%i in ('git describe --tags --always') do set VERSION=%%i
echo VERSION = "%VERSION%"> psu_mgmt\app\version.py

call nuitka ^
--msvc=latest ^
--standalone ^
--windows-disable-console ^
--enable-plugin=pyside6 ^
--output-filename=psu_mgmt ^
psu_mgmt/app/psu_mgmt.py

echo VERSION = "dev"> psu_mgmt\app\version.py
