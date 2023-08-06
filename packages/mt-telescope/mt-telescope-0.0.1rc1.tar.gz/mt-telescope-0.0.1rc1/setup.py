# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telescope',
 'telescope.filters',
 'telescope.metrics',
 'telescope.metrics.bertscore',
 'telescope.metrics.bleurt',
 'telescope.metrics.chrf',
 'telescope.metrics.comet',
 'telescope.metrics.gleu',
 'telescope.metrics.meteor',
 'telescope.metrics.prism',
 'telescope.metrics.sacrebleu',
 'telescope.metrics.ter',
 'telescope.metrics.zero_edit']

package_data = \
{'': ['*']}

install_requires = \
['bert-score==0.3.7',
 'fairseq==0.9.0',
 'numpy<1.20.0',
 'plotly>=4.14.3,<5.0.0',
 'pytorch-nlp==0.5.0',
 'sacrebleu>=1.4.8',
 'scipy==1.5.0',
 'stanza>=1.2,<2.0',
 'streamlit>=0.79.0,<0.80.0',
 'torch>=1.6.0',
 'unbabel-comet==1.0.0rc1']

entry_points = \
{'console_scripts': ['telescope = telescope.cli:telescope']}

setup_kwargs = {
    'name': 'mt-telescope',
    'version': '0.0.1rc1',
    'description': 'A visual platform for contrastive evaluation of machine translation systems',
    'long_description': '<p align="center">\n  <img src="https://user-images.githubusercontent.com/17256847/124762084-66212200-df2a-11eb-92ce-edbebfe9d4e2.jpg">\n  <br />\n  <br />\n  <a href="https://github.com/Unbabel/MT-Telescope/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Unbabel/MT-Telescope" /></a>\n  <a href="https://github.com/Unbabel/MT-Telescope/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Unbabel/MT-Telescope" /></a>\n  <a href=""><img alt="PyPI" src="https://img.shields.io/pypi/v/mt-telescope" /></a>\n  <a href="https://github.com/psf/black"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-black" /></a>\n</p>\n\n\nMT-Telescope is a toolkit for comparative analysis of MT systems that provides a number of tools that add rigor and depth to MT evaluation. With this package we endeavour to make it easier for researchers and industry practitioners to compare MT systems by giving you easy access to:\n\n1) SOTA MT evaluation metrics such as COMET  [(rei, et al 2020)](https://aclanthology.org/2020.emnlp-main.213/).\n2) Statistical tests such as bootstrap resampling [(Koehn, et al 2004)](https://aclanthology.org/W04-3250/).\n3) Dynamic Filters to select parts of your testset with specific phenomena\n4) Visual interface/plots to compare systems side-by-side segment-by-segment.\n\nWe highly recommend reading the following papers to learn more about how to perform better MT-Evaluation:\n- [Scientific Credibility of Machine Translation Research: A Meta-Evaluation of 769 Papers](https://arxiv.org/pdf/2106.15195.pdf)\n- [To Ship or Not to Ship: An Extensive Evaluation of Automatic Metrics for Machine Translation](https://arxiv.org/pdf/2107.10821.pdf)\n\n\n## Install:\n\n### Via pip:\n\n```bash\npip install mt-telescope==0.0.1rc1\n```\n\nNote: This is a pre-release currently.\n\n### Locally:\nCreate a virtual environment and make sure you have [poetry](https://python-poetry.org/docs/#installation) installed.\n\nFinally run:\n\n```bash\ngit clone https://github.com/Unbabel/MT-Telescope\ncd MT-Telescope\npoetry install\n```\n\n## Scoring:\n\nTo get the system level scores for a particular MT simply run `telescope score`.\n\n```bash\ntelescope score -s {path/to/sources} -h {path/to/translations} -r {path/to/references} -l {target_language} -m COMET -m chrF\n```\n\n## Comparing two systems:\nFor comparison between two systems you can run telescope using:\n1. The command line interface\n2. A web browser\n\n### Command Line Interface (CLI):\n\nFor running system comparisons with CLI you should use the `telescope compare` command.\n\n```\nUsage: telescope compare [OPTIONS]\n\nOptions:\n  -s, --source FILENAME           Source segments.  [required]\n  -x, --system_x FILENAME         System X MT outputs.  [required]\n  -y, --system_y FILENAME         System Y MT outputs.  [required]\n  -r, --reference FILENAME        Reference segments.  [required]\n  -l, --language TEXT             Language of the evaluated text.  [required]\n  -m, --metric [COMET|sacreBLEU|chrF|ZeroEdit|BLEURT|BERTScore|TER|Prism|GLEU]\n                                  MT metric to run.  [required]\n  -f, --filter [named-entities|duplicates]\n                                  MT metric to run.\n  --seg_metric [COMET|ZeroEdit|BLEURT|BERTScore|Prism|GLEU]\n                                  Segment-level metric to use for segment-\n                                  level analysis.\n\n  -o, --output_folder TEXT        Folder you wish to use to save plots.\n  --bootstrap\n  --num_splits INTEGER            Number of random partitions used in\n                                  Bootstrap resampling.\n\n  --sample_ratio FLOAT            Folder you wish to use to save plots.\n  --help                          Show this message and exit.\n```\n\n#### Example 1: Running several metrics\n\nRunning BLEU, chrF BERTScore and COMET to compare two systems:\n\n```bash\ntelescope compare \\\n  -s path/to/src/file.txt \\\n  -x path/to/system-x/file.txt \\\n  -y path/to/system-y \\\n  -r path/to/ref/file.txt \\\n  -l en \\\n  -m BLEU -m chrF -m BERTScore -m COMET\n```\n\n#### Example 2: Saving a comparison report\n\n```bash\ntelescope compare \\\n  -s path/to/src/file.txt \\\n  -x path/to/system-x/file.txt \\\n  -y path/to/system-y \\\n  -r path/to/ref/file.txt \\\n  -l en \\\n  -m COMET \\\n  --output_folder FOLDER-PATH\n```\n\n### Web Interface\n\nTo run a web interface simply run:\n```bash\nstreamlit run app.py\n```\n\n\n# Cite:\n\n@inproceedings{rei-etal-2021-mt,\n  author = {Rei, Ricardo  and  Stewart, Craig  and  Farinha, Ana C  and  Lavie, Alon},\n    title = "{MT}-{T}elescope: {A}n interactive platform for contrastive evaluation of {MT} systems",\n    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Demonstrations)",\n    month = aug,\n    year = "2021",\n    address = "Online",\n    publisher = "Association for Computational Linguistics",\n}',
    'author': 'Ricardo Rei, Craig Stewart, Catarina Farinha, Alon Lavie',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unbabel/MT-Telescope',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
