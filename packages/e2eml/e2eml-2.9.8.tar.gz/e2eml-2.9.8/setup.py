from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["babel>=2.9.0",
                "boostaroota>=1.3",
                "catboost>=0.21",
                "category_encoders==2.3.0", # changed to also include newer versions
                "dill>=0.3.3",
                "imblearn>=0.0",
                "imgaug==0.2.5",
                "lightgbm==3.1.0",
                "matplotlib==3.1.3", # pinned due to cannot import _png error
                "ngboost>=0.3.1",
                "nltk>=3.2.4",
                "numpy>=1.19.4",
                "optuna>=2.5.0",
                "pandas==1.1.5",
                "pip>=21.0.1",
                "plotly==5.4.0",
                "psutil==5.8.0",
                "pytorch_tabnet>=3.1.1",
                "seaborn>=0.11.1",
                "scikit-learn>=1.0.1",
                "scipy>=1.5.4",  # 1.6.3 before
                "setuptools >= 51.1.0",
                "shap>=0.39.0",
                "spacy>=2.3.0",
                "textblob>=0.15.3",
                "torch >= 1.7.0",
                "transformers>=4.0.0",
                "vowpalwabbit>=8.11.0",
                "xgboost>=1.3.3",
                ]

extras_require = {
    'rapids': ['cupy>=8.1.0', 'cython>=0.29.21'],
    'jupyter': ['ipython>=7.10.0', 'jupyter_core>=4.7.0', 'notebook>=6.1.0'],
    'full': ['cupy>=8.1.0', 'cython>=0.29.21', 'ipython>=7.10.0', 'jupyter_core>=4.7.0', 'notebook>=6.1.0']
}

setup(
    name="e2eml",
    version="2.9.8",
    author="Thomas Meißner",
    author_email="meissnercorporation@gmx.de",
    description="An end to end solution for automl.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ThomasMeissnerDS/e2e_ml",
    packages=find_packages(),
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)