from setuptools import setup, find_packages

setup(name="server_project",
      version="0.0.1",
      description="mess_server_proj",
      author="FidelSol",
      author_email="fsoloviov2020@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
