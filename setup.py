from setuptools import setup

setup(name='py-ugs3client',
      version='0.1',
      description='UGS3 Python client',
      url='https://github.com/vsevolod-kolchinsky/py-ugs3client',
      author='Vsevolod Kolchinsky',
      author_email='vsevolod.kolchinsky@gmail.com',
      license='MIT',
      packages=['ugs3client'],
      install_requires=[
          'requests',
      ],
      )
