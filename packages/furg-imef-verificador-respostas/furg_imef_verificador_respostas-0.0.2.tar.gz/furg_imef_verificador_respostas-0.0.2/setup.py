from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="furg_imef_verificador_respostas",
    version='0.0.2',
    description="Verificador de respostas numéricas para problemas de laboratórios do IMEF.",
    long_description=long_description,
    url="https://github.com/LaboratorioIPythonFURG/verificador_respostas",
    author='FURG - IMEF',
    license='Unlicense',
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent"
    ],
    packages=['furg_imef_verificador_respostas'],
    python_requires=">=3.6"
)
