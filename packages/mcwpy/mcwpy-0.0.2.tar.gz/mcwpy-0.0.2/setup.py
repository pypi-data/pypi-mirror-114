from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='mcwpy',
    version='0.0.2',
    description='A new way to create Minecraft datapacks',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type='text/markdown',
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
