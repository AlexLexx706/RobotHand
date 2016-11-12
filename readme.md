Программа настроки и управления модели руки робота,
Также программа позволяет управлять реальной рукой робота в соответствии с настройками.

Устновка ubuntu:
---------
0. Установка PyQt: sudo apt-get install python-qt4 python-qt4-gl
1. Установка виртуального окружения: virtualenv venv --system-site-packages
2. Запуск виртуального окружения: source venv/bin/activate
2. Установка requirements: pip install -r requirements.txt
3. Установка приложения: python setup.py install

Запуск в виртуальном окружении:
-------------------------------
1. Запуск виртуального окружения: source venv/bin/activate
2. Запуск приложения: ./run_configurator.sh

Запуск:
-------
введите комманду: ./venv/bin/configurator

Усановка windows:
-----------------------
0. Установка виртуального окружения: virtualenv venv
1. Активация окружения: venv\Scripts\activate
2. Скачать: PyQt, numpy, scipy из http://www.lfd.uci.edu/~gohlke/pythonlibs
3. установка: pip install PyQt4-4.11.4-cp27-none-win_amd64.whl numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl scipy-0.18.1-cp27-cp27m-win_amd64.whl PyOpenGL-3.1.1-cp27-cp27m-win_amd64.whl
2. Установка requirements: pip install -r requirements.win.txt
3. Установка приложения: python setup.py install

Запуск:
-------
windows: venv\Scripts\configurator.exe
