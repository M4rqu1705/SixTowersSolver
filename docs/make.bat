@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)

if NOT "%2" == "" (
	set SPHINXOPTS="%2"
)


set SPHINXAUTODOC=sphinx-apidoc
set SOURCEDIR=source
set BUILDDIR=build
set AUTODOCDIR=source\autodoc
set PROGRAMSDIR=..\src\.


if "%1" == "" goto help
if "%1" == "clean" goto clean

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)


%SPHINXAUTODOC% -o %AUTODOCDIR% %PROGRAMSDIR% %O%
if "%SPHINXOPTS%" == "" (
  %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %O%

) else (
  echo.%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
  %SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

)

goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:clean
echo.Removing everything under %BUILDDIR% and %AUTODOCDIR% ...
rmdir %AUTODOCDIR% /S /Q
mkdir %AUTODOCDIR%
rmdir %BUILDDIR% /S /Q
mkdir %BUILDDIR%
goto end

:end
popd