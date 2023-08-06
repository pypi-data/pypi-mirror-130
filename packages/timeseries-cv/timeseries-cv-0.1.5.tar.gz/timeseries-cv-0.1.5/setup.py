# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsxv']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'timeseries-cv',
    'version': '0.1.5',
    'description': 'Timeseries cross-validation for Neural Networks',
    'long_description': '# Time-Series Cross-Validation\n\nThis python package aims to implement Time-Series Cross Validation Techniques.\n\nThe idea is given a training dataset, the package will split it into Train, Validation and Test sets, by means of either Forward Chaining, K-Fold or Group K-Fold.\n\nAs parameters the user can not only select the number of inputs (n_steps_input) and outputs (n_steps_forecast), but also the number of samples (n_steps_jump) to jump in the data to train.\n\nThe best way to install the package is as follows: `pip install timeseries-cv` and then use it with `import tsxv`.\n\n<!-- TABLE OF CONTENTS -->\n\n<ol>\n  <li>\n    <a href="#Features">Features</a>\n    <ul>\n      <li><a href="#split-train">Split Train</a></li>\n      <li><a href="#split-train-val">Split Train Val</a></li>\n      <li><a href="#split-train-val-test">Split Train Val Test</a></li>\n    </ul>\n  </li>\n  <li><a href="#Citation">Citation</a></li>\n</ol>\n\n\n## Features\n\nThis can be seen more intuitively using the jupyter notebook: "example.ipynb"\nBelow you can find an example of the usage of each function for the following Time-Series:\n\n```\ntimeSeries = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26])\n```\n\n## Split Train\n\n#### split_train\n```\nfrom tsxv.splitTrain import split_train\nX, y = split_train(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="756" alt="train" src="https://user-images.githubusercontent.com/25267873/74095694-37600b80-4aec-11ea-979e-1bd50ed5851a.png">\n\n#### split_train_variableInput\n```\nfrom tsxv.splitTrain import split_train_variableInput\nX, y = split_train_variableInput(timeSeries, minSamplesTrain=10, n_steps_forecast=3, n_steps_jump=3)\n```\n\n![split_train_variableInput](https://user-images.githubusercontent.com/25267873/76267051-67243f80-6261-11ea-9eba-8a25fa810b06.png)\n\n## Split Train Val\n\n#### split_train_val_forwardChaining\n```\nfrom tsxv.splitTrainVal import split_train_val_forwardChaining\nX, y, Xcv, ycv = split_train_val_forwardChaining(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="742" alt="trainVal - forwardChaining" src="https://user-images.githubusercontent.com/25267873/74094568-720d7800-4adb-11ea-8d69-7c1cbd6774c7.png">\n\n#### split_train_val_kFold\n```\nfrom tsxv.splitTrainVal import split_train_val_kFold\nX, y, Xcv, ycv = split_train_val_kFold(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="743" alt="trainVal - kFold" src="https://user-images.githubusercontent.com/25267873/74094572-746fd200-4adb-11ea-91fd-93935d51982f.png">\n\n#### split_train_val_groupKFold\n```\nfrom tsxv.splitTrainVal import split_train_val_groupKFold\nX, y, Xcv, ycv = split_train_val_groupKFold(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="744" alt="trainVal - groupKFold" src="https://user-images.githubusercontent.com/25267873/74094569-72a60e80-4adb-11ea-8345-1233b0a47e2e.png">\n\n\n## Split Train Val Test\n\n#### split_train_val_test_forwardChaining\n\n```\nfrom tsxv.splitTrainValTest import split_train_val_test_forwardChaining\nX, y, Xcv, ycv, Xtest, ytest = split_train_val_test_forwardChaining(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="744" alt="trainValTest - forwardChaining" src="https://user-images.githubusercontent.com/25267873/74094566-6fab1e00-4adb-11ea-810d-e085518c3cb5.png">\n\n#### split_train_val_test_kFold\n```\nfrom tsxv.splitTrainValTest import split_train_val_test_kFold\nX, y, Xcv, ycv, Xtest, ytest = split_train_val_test_kFold(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="745" alt="trainValTest - kFold" src="https://user-images.githubusercontent.com/25267873/74094570-73d73b80-4adb-11ea-94cd-5ab4d02c8cbf.png">\n\n#### split_train_val_test_groupKFold\n```\nfrom tsxv.splitTrainValTest import split_train_val_test_groupKFold\nX, y, Xcv, ycv, Xtest, ytest = split_train_val_test_groupKFold(timeSeries, n_steps_input=4, n_steps_forecast=3, n_steps_jump=2)\n```\n\n<img width="744" alt="trainValTest - groupKFold" src="https://user-images.githubusercontent.com/25267873/74094567-70dc4b00-4adb-11ea-994b-c3f1727f4b83.png">\n\n\n## Citation\n\nThis module was developed with co-autorship with Filipe Roberto Ramos (https://ciencia.iscte-iul.pt/authors/filipe-roberto-de-jesus-ramos/cv) for his phD thesis entitled "Data Science in the Modeling and Forecasting of Financial timeseries: from Classic methodologies to Deep Learning". Submitted in 2021 to Instituto Universitário de Lisboa - ISCTE Business School, Lisboa, Portugal.\n\nAPA \n\n`Ramos, F. (2021). Data Science na Modelação e Previsão de Séries Económico-financeiras: das Metodologias Clássicas ao Deep Learning. (PhD Thesis submitted, Instituto Universitário de Lisboa - ISCTE Business School, Lisboa, Portugal).`\n\n```\n@phdthesis{FRRamos2021,\n      AUTHOR = {Filipe R. Ramos},\n      TITLE = {Data Science na Modelação e Previsão de Séries Económico-financeiras: das Metodologias Clássicas ao Deep Learning},\n      PUBLISHER = {PhD Thesis submitted, Instituto Universitário de Lisboa - ISCTE Business School, Lisboa, Portugal},\n      YEAR =  {2021}\n}\n```\n',
    'author': 'didier',
    'author_email': 'dro.lopes@campus.fct.unl.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DidierRLopes/timeseries-cv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
