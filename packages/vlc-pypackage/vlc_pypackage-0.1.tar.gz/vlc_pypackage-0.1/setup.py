from setuptools import setup, find_packages

pkg_name = "vlc_pypackage"

setup(name=pkg_name,
      version='0.1',
      description='Bad Joke for educational purposes only',
      url='https://github.com/VLavado/vlc_pypackage',
      author='VLC',
      author_email='vlc@example.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)