"""
py setup.py sdist
twine upload dist/expressmoney-0.50.5.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='0.60.0',
    description='SDK ExpressMoney',
    author='Sergey Zherebtsov',
    author_email='sergey@expressmoney.com',
    url='https://github.com/zsergey85/',
    install_requires=('google-cloud-secret-manager', 'google-cloud-error-reporting', 'google-cloud-pubsub',
                      'google-cloud-tasks', 'google-cloud-storage'),
    download_url='https://github.com/zsergey85/',
    keywords=('expressmoney',),
    classifiers=(),
    python_requires='>=3.7',
)
