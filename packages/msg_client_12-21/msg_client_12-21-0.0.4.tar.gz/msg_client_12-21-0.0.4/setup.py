from setuptools import setup, find_packages

setup(name='msg_client_12-21',
      version='0.0.4',
      description='The client part of the course project "Messenger"',
      author='Kostitsyn Aleksandr',
      author_email='kostitsin.a@mail.ru',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      )