import setuptools

setuptools.setup(name='deteefapi',
                 version='0.4.1',
                 description='API for daily telegraf',
                 url='',
                 author='Smyek',
                 author_email='smyek.job@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=['requests', 'ratelimit'],
                 zip_safe=False)
