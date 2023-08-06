#from distutils.core import setup
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
name="GaERP", # Nombre de la app (CamelCase)
version="1.0", # Versión
author="Gonzalo G. Campos", # Nombre del Autor
author_email="gonzalo.g.campos@gmail.com", # E-mail del autor
packages=["GaERP"], # Paquetes a incluir
package_dir = {'GaERP':'/home/ggc/fuentes/GaERP'},
license="GPL v3.0", # Licencia
# Descripción corta
description="Gestión Almacen + Contabilidad",
long_description=open('README.txt').read(), # Descripción larga
url='https://pypi.python.org/pypi/GaERP',
classifiers=[
"Development Status :: 5 - Production/Stable",
"Environment :: Console",
"Intended Audience :: Developers",
"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
"Natural Language :: Spanish",
"Operating System :: OS Independent",
"Programming Language :: Python :: 3.8",
"Programming Language :: Python :: 3 :: Only",
"Topic :: Software Development",
"Topic :: Software Development :: Libraries :: Python Modules"
],
keywords='GaERP contabilidad almacen',
)

