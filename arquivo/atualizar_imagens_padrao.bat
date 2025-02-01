@echo off
setlocal enabledelayedexpansion

REM Caminho para a pasta de imagens
set "path_imagens=imagens"
cd /d "%path_imagens%"

REM Contadores para nomes sequenciais
set count_with_txt=1
set count_without_txt=1

REM Renomear arquivos com .txt correspondentes
echo Renomeando arquivos com labels...
for %%F in (*.jpg) do (
    if exist "%%~nF.txt" (
        set "base_name=img_!count_with_txt!"
        ren "%%F" "!base_name!.jpg"
        ren "%%~nF.txt" "!base_name!.txt"
        echo Renomeando: %%F para !base_name!.jpg e !base_name!.txt
        set /a count_with_txt+=1
    )
)

REM Renomear arquivos sem .txt correspondentes
echo Renomeando arquivos sem labels...
for %%F in (*.jpg) do (
    if not exist "%%~nF.txt" (
        set "base_name=img_!count_with_txt!"
        ren "%%F" "!base_name!.jpg"
        echo Renomeando: %%F para !base_name!.jpg
        set /a count_with_txt+=1
    )
)

echo Imagens renomeadas para padrao sequencial.
pause
