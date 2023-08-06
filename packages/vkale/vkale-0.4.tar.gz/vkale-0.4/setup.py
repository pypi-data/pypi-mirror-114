import setuptools

setuptools.setup(name='vkale',
                 version='0.4',
                 description='API for VK',
                 url='',
                 author='Smyek',
                 author_email='smyek.job@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=['requests', 'ratelimit'],
                 zip_safe=False)