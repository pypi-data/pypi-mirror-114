from setuptools import _install_setup_requires, setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='mcwpy',
    version='0.0.0',
    description='Add a new way to create Minecraft datapacks',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='Vianpyro',
    author_email='vianney.veremme@gmail.com',
    url='https://github.com/vianneyveremme/minecraft_with_python',
    license='MIT',
    keywords=['Minecraft', 'Datapack', 'Function', 'MCFunction'],
    classifiers=classifiers,
    packages=find_packages(exclude=['tests']),
    install_requires=open('REQUIREMENTS.txt').read(),
    zip_safe=False
)
