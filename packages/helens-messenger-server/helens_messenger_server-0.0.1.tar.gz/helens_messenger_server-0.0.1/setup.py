from setuptools import setup, find_packages

setup(name="helens_messenger_server",
      version="0.0.1",
      description="helens_messenger - server part",
      author="Helen Maksimova",
      author_email="djushiro@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
