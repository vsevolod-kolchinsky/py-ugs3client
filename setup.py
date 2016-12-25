from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='py-ugs3client',
      version='0.9.0',
      description='UGS3 Python client',
      long_description=readme(),
      classifiers=[
                   'Development Status :: 4 - Beta',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      url='https://github.com/vsevolod-kolchinsky/py-ugs3client',
      author='Vsevolod Kolchinsky',
      author_email='vsevolod.kolchinsky@gmail.com',
      license='Apache Software License',
      packages=['ugs3client'],
      install_requires=[
          'requests','cached-property','pymemcache',
      ],
      )
