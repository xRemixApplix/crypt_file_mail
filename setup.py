"""
    Script de creation de l'executable du programme
"""
from cx_Freeze import setup, Executable
BASE = None

EXECUTABLES = [Executable("auto.py", base=BASE)]

PACKAGES = [
    "idna",
    "xlrd",
    "module/code_file",
    "module/conso_file",
    "module/mail",
    "module/csv"
]

OPTIONS = {
    'build_exe': {
        'packages': PACKAGES,
    },
}

setup(
    name="Crypt_File_Mail",
    options=OPTIONS,
    version="0.5",
    description="Envoi automatique d'un mail de conso",
    executables=EXECUTABLES
)
