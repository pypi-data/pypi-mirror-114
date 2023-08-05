from setuptools import setup,find_packages
setup(
    name="donotimport",
    version="0.0.2",
    author="Yasser Bdj (Boudjada Yasser)",
    author_email="yasser.bdj96@gmail.com",
    description='''A simple package to prevent the abusive use of the import statement in Python.''',
    long_description_content_type="text/markdown",
    long_description=open('README.md','r').read(),
    license='''MIT License''',
    packages=find_packages(),
    url="https://github.com/yasserbdj96/donotimport",
    project_urls={
        'Author WebSite': "https://yasserbdj96.github.io/",
    },
    install_requires=[''],
    keywords=['yasserbdj96', 'python', 'donotimport', 'A', 'simple', 'package', 'to', 'prevent', 'the', 'abusive', 'use', 'of', 'the', 'import', 'statement', 'in', 'Python.'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Topic :: Communications :: Email'
    ],
    python_requires=">=3.x.x"
)