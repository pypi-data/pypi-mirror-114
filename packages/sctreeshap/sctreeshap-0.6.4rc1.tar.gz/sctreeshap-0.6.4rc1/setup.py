import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
  long_description = fh.read()

setuptools.setup(
  name="sctreeshap",
  version="0.6.4.rc1",
  author="Haoxuan Xie",
  author_email="haoxuanxie@link.cuhk.edu.cn",
  url="https://github.com/ForwardStar/sctreeshap",
  py_modules=["sctreeshap"],
  description="sctreeshap: a cluster tree data structure, and for shap analysis",
  long_description=long_description,
  long_description_content_type="text/markdown",
  license="LICENSE",
  classifiers=[
  "Programming Language :: Python :: 3.5",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  install_requires=['shap',
                    'matplotlib',
                    'anndata',
                    'numpy',
                    'pandas',
                    'sklearn',
                    'scikit-learn',
                    'imblearn',
                    'imbalanced-learn',
                    'xgboost',
                    'loompy',
                    'tqdm',
                    'requests',
                    'pathlib',
                    'pip'],
  python_requires='>=3.5'
)
