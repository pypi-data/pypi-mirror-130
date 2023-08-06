from setuptools import setup, find_packages

setup(name="server_project_1",
      version="0.0.3",
      description="mess_server_proj_1",
      author="FidelSol",
      author_email="fsoloviov2020@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
