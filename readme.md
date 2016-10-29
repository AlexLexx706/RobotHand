Программа настроки и управления модели руки робота,
Также программа позволяет управлять реальной рукой робота в соответствии с настройками.

Устновка ubuntu:
---------
0. Установка виртуального окружения: virtualenv venv && source venv/bin/activate
1. Установка PyQt: apt-get install python-qt4 python-qt4-gl
2. Установка requirements: pip install -r requirements.txt
3. Установка приложения: python setup.py install

Усановка windows 7:
-----------------------
0. Установка виртуального окружения: virtualenv venv
1. Активация окружения: venv\Scripts\activate
2. Скачать: PyQt, numpy, scipy из http://www.lfd.uci.edu/~gohlke/pythonlibs
3. установка: pip install PyQt4-4.11.4-cp27-none-win_amd64.whl numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl scipy-0.18.1-cp27-cp27m-win_amd64.whl PyOpenGL-3.1.1-cp27-cp27m-win_amd64.whl
2. Установка requirements: pip install -r requirements.win.txt
3. Установка приложения: python setup.py install

Запуск:
-------

linux: ./venv/bin/configurator
windows: venv\Scripts\configurator.exe