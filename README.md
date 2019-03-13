# AwAI

To visualize the GUI, you need to have Qt5 installed.

## On Linux Ubuntu/Debian

**QT 5**
``` bash
sudo apt install build-essential
sudo apt install qt5-default
```
**Qt5 documentation**
```bash
sudo apt install qt5-doc
sudo apt install qt5-doc-html qtbase5-doc-html
sudo apt install qtbase5-examples
```

**Qt5 for Python**
```bash
sudo apt install python3-pyqt5 pyqt5-dev-tools
```

**QtCreator**
To edit the .ui file and bring modifications to the GUI, you will need QtCreator and QtDesigner 
```bash
sudo apt install qtcreator
```

**To generate the Python code from the .ui, you have to execute**
```bash
pyuic5 -x gui.ui -o gui.py
pyrcc5 image.qrc -o image_rc.py
```
