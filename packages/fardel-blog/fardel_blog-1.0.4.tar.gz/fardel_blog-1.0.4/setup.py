from setuptools import setup, find_packages


install_requires = [
    "fardel==1.3.5",
]

setup(
    name='fardel_blog',
    version='1.0.4',
    description='Blog plugin for Fardel CMS',
    author='Sepehr Hamzehlouy',
    author_email='s.hamzelooy@gmail.com',
    url='https://github.com/FardelCMS/fardel_ecommerce',
    packages=find_packages(".", exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={
        'static': ['*.html'],
    },
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.7',
    ],
)
