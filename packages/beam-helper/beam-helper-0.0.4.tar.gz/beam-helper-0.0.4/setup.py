from setuptools import setup
setup(name="beam-helper",
      version="0.0.4",
      author="chris",
      author_email="christopherpearce10@gmail.com",
      install_requires=['wheel', 'pandas >= 1.2.4', 'numpy >= 1.19.5', 'apache-beam >= 2.29'],
      packages=['beam_helper'],
      include_package_data=True)
