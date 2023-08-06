# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pcmf']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'pcmf',
    'version': '0.1.1',
    'description': 'PCMF is a Python package of Positive Collective Matrix Factorization(PCMF). PCMF is a model that combines the interpretability of NMF and the extensibility of CMF.',
    'long_description': '![](https://raw.githubusercontent.com/N-YS-KK/PCMF/main/images/PCMF_logo.PNG) \n\n# Positive Collective Matrix Factorization (PCMF)\nWe propose Positive Collective Matrix Factorization (PCMF). PCMF is a model that combines the interpretability of NMF and the extensibility of CMF.\n\n# Description of PCMF\nNon-Negative Matrix Factorization (NMF) and Collective matrix Factorization (CMF) exist as methods of matrix factorization. The features of each are as follows.\n\n## Non-Negative Matrix Factorization（NMF）\nPredict the original matrix by the product of two nonnegative matrices.\n\n![](https://raw.githubusercontent.com/N-YS-KK/PCMF/main/images/NMF.PNG) \n\n- Advantages  \n\nSince it is non-negative, a highly interpretable feature representation can be obtained.\n\n- Disadvantages  \n\nLow extensibility because multiple relationships cannot be considered.\n\n## Collective matrix Factorization（CMF）\nThis is a method of factoring two or more relational data (matrix) at the same time when a set has multiple relations.\n\n![](https://raw.githubusercontent.com/N-YS-KK/PCMF/main/images/CMF.PNG) \n\n- Advantages  \n\nIn addition to being able to consider multiple relationships, flexible output is possible (link function), so it is highly extensible.\n\n- Disadvantages  \n\nThe interpretability is low because positive and negative values appear in the elements of the matrix.\n\n## Positive Collective Matrix Factorization (PCMF)\nPCMF is a model that combines the advantages of NMF, "interpretability," and the advantages of CMF, "extensibility." Specifically, for each matrix, interpretability is achieved by converting the elements of the matrix into positive values using a softplus function. The backpropagation method is used as the learning method.\n\n![](https://raw.githubusercontent.com/N-YS-KK/PCMF/main/images/PCMF.PNG) \n\n# Installation\ncoming soon!\n\n# Usage\ncoming soon!\n\n# Training\ncoming soon!\n\n# License\nMIT Licence\n\n# Joint research\ncoming soon!\n\n# Citation\ncoming soon!\n\n# Reference\n[1] Daniel D. Lee and H. Sebastian Seung. “Learning the parts of objects by non-negative matrix factorization.” Nature 401.6755 (1999): 788-791.\n\n[2] Daniel D. Lee and H. Sebastian Seung. “Algorithms for non-negative matrix factorization.” Advances in neural information processing systems 13 (2001): 556-562.\n\n[3] Ajit P. Singh and Geoffrey J. Gordon. Relational learning via collective matrix factorization. Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining: 650-658, 2008.\n\n[4] David E. Rumelhart, Geoffrey E. Hinton and Ronald J. Williams. “Learning representations by back-propagating errors.” Nature 323.6088 (1986): 533-536\n\n[5] Diederik P. Kingma and Jimmy Ba. “Adam: A method for stochastic optimization.” arXiv preprint arXiv:1412.6980 (2014).\n\n[6] Martín Abadi, Ashish Agarwal, Paul Barham, Eugene Brevdo, Zhifeng Chen, Craig Citro, Greg S. Corrado, Andy Davis, Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Ian Goodfel-low, Andrew Harp, Geoffrey Irving, Michael Isard, Yangqing Jia, Rafal Jozefowicz, Lukasz Kaiser, Manjunath Kudlur, Josh Levenberg, Dan Mane, Rajat Monga, Sherry Moore, Derek Murray, Chris Olah, Mike Schuster, Jonathon Shlens, Benoit Steiner, Ilya Sutskever, Kunal Talwar, Paul Tucker, Vincent Vanhoucke, Vijay Vasudevan, Fernanda Viegas, Oriol Vinyals, Pete Warden, Martin Wattenberg, Martin Wicke, Yuan Yu and Xiaoqiang Zheng. “Tensor-flow: Large-scale machine learning on heterogeneous distributed systems.” arXiv preprint arXiv:1603.04467 (2016)\n',
    'author': 'Y. Sumiya',
    'author_email': 'y.sumiya.1031@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/N-YS-KK',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
