$VCPKG_TRIPLET = 'my-x86-windows-static'

$startloc = $PSScriptRoot

$VCPKG_RT = ${env:VCPKG_ROOT}
if ($null -eq $VCPKG_RT)
{
	Write-Warning "Could not find VCPKG_ROOT. Please set up vcpkg environment."
	exit
}

$VCPKG_EXE = "$VCPKG_RT\vcpkg.exe"
if (!(Test-Path $VCPKG_EXE)){
	Write-Warning "Invalid VCPKG_ROOT. Please check vcpkg environment."
	exit
}

$TRIPLET_TARGET = "$VCPKG_RT\triplets\$VCPKG_TRIPLET.cmake"

Write-Host "Vcpkg root found at : $env:VCPKG_ROOT" -ForegroundColor Green
Write-Host "Creating triplets : $VCPKG_TRIPLET"-ForegroundColor Green
Write-Output 'set(VCPKG_TARGET_ARCHITECTURE x86)'	| Out-File -FilePath $TRIPLET_TARGET -Encoding utf8
Write-Output 'set(VCPKG_CRT_LINKAGE dynamic)' 		| Out-File -FilePath $TRIPLET_TARGET -Encoding utf8 -Append
Write-Output 'set(VCPKG_LIBRARY_LINKAGE static)' 	| Out-File -FilePath $TRIPLET_TARGET -Encoding utf8 -Append
Write-Output 'set(VCPKG_PLATFORM_TOOLSET v141)'   	| Out-File -FilePath $TRIPLET_TARGET -Encoding utf8 -Append

Write-Host "Building denpendecies..."
Set-Location -Path $VCPKG_RT
.\vcpkg --triplet $VCPKG_TRIPLET install libiconv boost-algorithm
Set-Location -Path $startloc
Write-Host "Building of dependencies completed." -ForegroundColor Green