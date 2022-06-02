from PyQt5 import uic
with open("login_pythonUI.py","w",encoding="utf-8") as fout:
    uic.compileUi('login_python.ui',fout)