# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyloras']

package_data = \
{'': ['*']}

install_requires = \
['imbalanced-learn>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'pyloras',
    'version': '0.1.0b3',
    'description': 'LoRAS: An oversampling approach for imbalanced datasets',
    'long_description': "# LoRAS\n\n[![CI][3]](https://github.com/zoj613/pyloras/actions/workflows/build-and-test.yml)\n[![Codecov][4]](https://codecov.io/gh/zoj613/pyloras/)\n[![PyPI][5]](https://pypi.org/project/pyloras/#history)\n\nLocalized Random Affine Shadowsampling\n\nThis repo provides a python implementation of an imbalanced dataset oversampling\ntechnique known as Localized Random Affine Shadowsampling (LoRAS). This implementation \npiggybacks off the package ``imbalanced-learn`` and thus aims to be as compatible\nas possible with it.\n\n\n## Dependencies\n- `imbalanced-learn`\n\n\n## Installation\n\nUsing `pip`:\n```shell\n$ pip install -U pyloras\n```\n\nInstalling from source requires an installation of [poetry][1] and the following shell commands:\n```shell\n$ git clone https://github.com/zoj613/pyloras.git\n$ cd pyloras/\n$ poetry install\n# add package to python's path\n$ export PYTHONPATH=$PWD:$PYTHONPATH \n```\n\n## Usage\n\n```python\nfrom collections import Counter\nfrom pyloras import LORAS\nfrom sklearn.datasets import make_classification\n\nX, y = make_classification(n_samples=20000, n_features=5, n_informative=5,\n                           n_redundant=0, n_repeated=0, n_classes=3,\n                           n_clusters_per_class=1,\n                           weights=[0.01, 0.05, 0.94],\n                           class_sep=0.8, random_state=0)\n\nlrs = LORAS(random_state=0, manifold_learner_params={'perplexity': 35, 'n_iter': 250})\nprint(sorted(Counter(y).items()))\n# [(0, 270), (1, 1056), (2, 18674)]\nX_resampled, y_resampled = lrs.fit_resample(X, y)\nprint(sorted(Counter(y_resampled.astype(int)).items()))\n# [(0, 18674), (1, 18674), (2, 18674)]\n\n# one can also use any custom 2d manifold learner via the ``manifold_learner` parameter\nfrom umap import UMAP\nLORAS(manifold_learner=UMAP()).fit_resample(X, y)\n\n```\n\n## Visualization\n\nBelow is a comparision of `imbalanced-learn`'s `SMOTE` implementation with `LORAS`\non the dummy data used in [this doc page][2] using the default parameters.\n\n![](./scripts/img/resampled_data.svg)\n![](./scripts/img/decision_fn.svg)\n![](./scripts/img/particularities.svg)\n\nThe plots can be reproduced by running:\n```\n$ python scripts/compare_oversamplers.py --n_neighbors=<optional> --n_shadow=<optional> --n_affine=<optional>\n```\n\n## References\nBej, S., Davtyan, N., Wolfien, M. et al. LoRAS: an oversampling approach for imbalanced datasets. Mach Learn 110, 279–301 (2021). https://doi.org/10.1007/s10994-020-05913-4\n\n\n[1]: https://python-poetry.org/docs/pyproject/\n[2]: https://imbalanced-learn.org/stable/auto_examples/over-sampling/plot_comparison_over_sampling.html#more-advanced-over-sampling-using-adasyn-and-smote\n[3]: https://img.shields.io/github/workflow/status/zoj613/pyloras/CI/main?style=flat-square\n[4]: https://img.shields.io/codecov/c/github/zoj613/pyloras?style=flat-square\n[5]: https://img.shields.io/github/v/release/zoj613/pyloras?include_prereleases&style=flat-square\n",
    'author': 'Zolisa Bleki',
    'author_email': 'zolisa.bleki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zoj613/pyloras/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
