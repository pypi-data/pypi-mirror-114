# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup', 'text_dedup.embed', 'text_dedup.suffix', 'text_dedup.utils']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'annoy>=1.17.0,<2.0.0',
 'coverage>=5.5,<6.0',
 'datasets>=1.5.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pytest-benchmark>=3.2.3,<4.0.0',
 'pytest>=6.2.2,<7.0.0',
 'sentence-transformers>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.0.10',
    'description': 'Text deduplication with fuzzy match and more',
    'long_description': '# text-dedup\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/cc66178e49d24908ac1fb2b2dbe4e5b3)](https://www.codacy.com/gh/ChenghaoMou/text-dedup/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/text-dedup&utm_campaign=Badge_Coverage) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc66178e49d24908ac1fb2b2dbe4e5b3)](https://www.codacy.com/gh/ChenghaoMou/text-dedup/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/text-dedup&utm_campaign=Badge_Grade)\n\n## Features\n\n-   SOTA embeddings with sentence-transformer\n-   Fast de-duplication with annoy\n-   [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499)\n\n## Installation\n\n```bash\npip install text-dedup\n```\n\n## Usage\n\n```python\nfrom text_dedup import SentenceTransformerDeduper\n\ndf = pd.read_csv(\'...\')\n\ndeduper = SentenceTransformerDeduper("distilbert-base-nli-stsb-mean-tokens")\ndf["group"] = deduper.group(df["text"].values.tolist(), show_progress_bar=True)\n\n# dedup with group indices\ndf = df.drop_duplicates(["group"], keep="first")\n```\n\n```python\nfrom text_dedup import SuffixArray\n\ndf = pd.read_csv(\'...\')\n\ndeduper = SuffixArray(k=50)\ngroups, duplicates = deduper.fit_transform(df["text"].values.tolist())\n\nassert len(groups) == len(df), "Invalid number of rows"\nassert len(duplicates) == groups.shape[1], "Invalid number of columns"\n```\n\n## Benchmark (w/ a P100)\n\n20k(5%) QQP subset\n\n```text\n              precision    recall  f1-score   support\n\n       False       0.75      0.89      0.81     12671\n        True       0.73      0.50      0.60      7543\n\n    accuracy                           0.75     20214\n   macro avg       0.74      0.70      0.71     20214\nweighted avg       0.74      0.75      0.73     20214\n\n\n--------------------------------------------- benchmark: 1 tests --------------------------------------------\nName (time in s)         Min      Max     Mean  StdDev   Median     IQR  Outliers     OPS  Rounds  Iterations\n-------------------------------------------------------------------------------------------------------------\ntest_scaling         89.9221  89.9221  89.9221  0.0000  89.9221  0.0000       0;0  0.0111       1          10\n-------------------------------------------------------------------------------------------------------------\n```\n',
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
