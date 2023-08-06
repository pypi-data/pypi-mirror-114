# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comet',
 'comet.cli',
 'comet.encoders',
 'comet.models',
 'comet.models.ranking',
 'comet.models.regression',
 'comet.modules']

package_data = \
{'': ['*']}

install_requires = \
['jsonargparse==3.13.1',
 'pandas==1.1.5',
 'pytorch-lightning==1.3.5',
 'sentencepiece>=0.1.96,<0.2.0',
 'transformers>=4.8.2,<5.0.0']

entry_points = \
{'console_scripts': ['comet-score = comet.cli.score:score_command',
                     'comet-train = comet.cli.train:train_command']}

setup_kwargs = {
    'name': 'unbabel-comet',
    'version': '1.0.0rc1',
    'description': 'High-quality Machine Translation Evaluation',
    'long_description': '<p align="center">\n  <img src="https://raw.githubusercontent.com/Unbabel/COMET/master/docs/source/_static/img/COMET_lockup-dark.png">\n  <br />\n  <br />\n  <a href="https://github.com/Unbabel/COMET/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Unbabel/COMET" /></a>\n  <a href="https://github.com/Unbabel/COMET/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Unbabel/COMET" /></a>\n  <a href=""><img alt="PyPI" src="https://img.shields.io/pypi/v/unbabel-comet" /></a>\n  <a href="https://github.com/psf/black"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-black" /></a>\n</p>\n\n\n## Quick Installation\n\nDetailed usage examples and instructions can be found in the [Full Documentation](https://unbabel.github.io/COMET/html/index.html).\n\nSimple installation from PyPI\n\n```bash\npip install unbabel-comet\n```\n\nTo develop locally install [Poetry](https://python-poetry.org/docs/#installation) and run the following commands:\n```bash\ngit clone https://github.com/Unbabel/COMET\npoetry install\n```\n\n## Scoring MT outputs:\n\n### Via Bash:\n\nExamples from WMT20:\n\n```bash\necho -e "Dem Feuer konnte Einhalt geboten werden\\nSchulen und Kindergärten wurden eröffnet." >> src.de\necho -e "The fire could be stopped\\nSchools and kindergartens were open" >> hyp.en\necho -e "They were able to control the fire.\\nSchools and kindergartens opened" >> ref.en\n```\n\n```bash\ncomet-score -s src.de -t hyp.en -r ref.en\n```\n\nYou can select another model/metric with the --model flag and for reference-less (QE-as-a-metric) models you dont need to pass a reference.\n\n```bash\ncomet-score -s src.de -t hyp.en -r ref.en --model refless-wmt21-large-da-1520\n```\n\nFollowing the work on [Uncertainty-Aware MT Evaluation]() you can use the --mc_dropout flag to get a variance/uncertainty value for each segment score. If this value is high, it means that the metric as less confidence is that prediction.\n\n```bash\ncomet-score -s src.de -t hyp.en -r ref.en --mc_dropout 100\n```\n\n## Languages Covered:\n\nAll the above mentioned models are build on top of XLM-R which cover the following languages:\n\nAfrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Basque, Belarusian, Bengali, Bengali Romanized, Bosnian, Breton, Bulgarian, Burmese, Burmese, Catalan, Chinese (Simplified), Chinese (Traditional), Croatian, Czech, Danish, Dutch, English, Esperanto, Estonian, Filipino, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Hausa, Hebrew, Hindi, Hindi Romanized, Hungarian, Icelandic, Indonesian, Irish, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Kurdish (Kurmanji), Kyrgyz, Lao, Latin, Latvian, Lithuanian, Macedonian, Malagasy, Malay, Malayalam, Marathi, Mongolian, Nepali, Norwegian, Oriya, Oromo, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskri, Scottish, Gaelic, Serbian, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tamil, Tamil Romanized, Telugu, Telugu Romanized, Thai, Turkish, Ukrainian, Urdu, Urdu Romanized, Uyghur, Uzbek, Vietnamese, Welsh, Western, Frisian, Xhosa, Yiddish.\n\n**Thus, results for language pairs containing uncovered languages are unreliable!**\n\n### Scoring within Python:\n\nCOMET implements the [Pytorch-Lightning model interface](https://pytorch-lightning.readthedocs.io/en/1.3.8/common/lightning_module.html) which means that you\'ll need to initialize a trainer in order to run inference.\n\n```python\nimport torch\nfrom comet import download_model, load_from_checkpoint\nfrom pytorch_lightning.trainer.trainer import Trainer\nfrom torch.utils.data import DataLoader\n\nmodel = load_from_checkpoint(\n  download_model("wmt21-small-da-152012")\n)\ndata = [\n    {\n        "src": "Dem Feuer konnte Einhalt geboten werden",\n        "mt": "The fire could be stopped",\n        "ref": "They were able to control the fire."\n    },\n    {\n        "src": "Schulen und Kindergärten wurden eröffnet.",\n        "mt": "Schools and kindergartens were open",\n        "ref": "Schools and kindergartens opened"\n    }\n]\ndata = [dict(zip(data, t)) for t in zip(*data.values())]\ndataloader = DataLoader(\n  dataset=data,\n  batch_size=16,\n  collate_fn=lambda x: model.prepare_sample(x, inference=True),\n  num_workers=4,\n)\ntrainer = Trainer(gpus=1, deterministic=True, logger=False)\npredictions = trainer.predict(\n  model, dataloaders=dataloader, return_predictions=True\n)\npredictions = torch.cat(predictions, dim=0).tolist()\n```\n\n**Note:** Using the python interface you will get a list of segment-level scores. You can obtain the corpus-level score by averaging the segment-level scores\n\n## Model Zoo:\n\n:TODO: Update model zoo after the shared task.\n\n| Model              |               Description                        |\n| :--------------------- | :------------------------------------------------ |\n| ↑`wmt21-large-da-1520` | **RECOMMENDED:** Regression model build on top of XLM-R (large) trained on DA from WMT15, to WMT20 |\n| ↑`wmt21-small-da-152012` | Same as the model above but trained on a small version of XLM-R that was distilled from XLM-R large |\n\n#### QE-as-a-metric:\n\n| Model              |               Description                        |\n| -------------------- | -------------------------------- |\n| `refless-wmt21-large-da-1520` | Reference-less model trained on top of XLM-R large with DAs from WMT15 to WMT20. |\n\n## Train your own Metric: \n\nInstead of using pretrained models your can train your own model with the following command:\n```bash\ncomet-train -cfg configs/models/{your_model_config}.yaml\n```\n\n### Tensorboard:\n\nLaunch tensorboard with:\n```bash\ntensorboard --logdir="lightning_logs/"\n```\n\n## unittest:\nIn order to run the toolkit tests you must run the following command:\n\n```bash\ncoverage run --source=comet -m unittest discover\ncoverage report -m\n```\n\n## Publications\n\n```\n@inproceedings{rei-etal-2020-comet,\n    title = "{COMET}: A Neural Framework for {MT} Evaluation",\n    author = "Rei, Ricardo  and\n      Stewart, Craig  and\n      Farinha, Ana C  and\n      Lavie, Alon",\n    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",\n    month = nov,\n    year = "2020",\n    address = "Online",\n    publisher = "Association for Computational Linguistics",\n    url = "https://www.aclweb.org/anthology/2020.emnlp-main.213",\n    pages = "2685--2702",\n}\n```\n\n```\n@inproceedings{rei-EtAl:2020:WMT,\n  author    = {Rei, Ricardo  and  Stewart, Craig  and  Farinha, Ana C  and  Lavie, Alon},\n  title     = {Unbabel\'s Participation in the WMT20 Metrics Shared Task},\n  booktitle      = {Proceedings of the Fifth Conference on Machine Translation},\n  month          = {November},\n  year           = {2020},\n  address        = {Online},\n  publisher      = {Association for Computational Linguistics},\n  pages     = {909--918},\n}\n```\n\n```\n@inproceedings{stewart-etal-2020-comet,\n    title = "{COMET} - Deploying a New State-of-the-art {MT} Evaluation Metric in Production",\n    author = "Stewart, Craig  and\n      Rei, Ricardo  and\n      Farinha, Catarina  and\n      Lavie, Alon",\n    booktitle = "Proceedings of the 14th Conference of the Association for Machine Translation in the Americas (Volume 2: User Track)",\n    month = oct,\n    year = "2020",\n    address = "Virtual",\n    publisher = "Association for Machine Translation in the Americas",\n    url = "https://www.aclweb.org/anthology/2020.amta-user.4",\n    pages = "78--109",\n}\n```\n',
    'author': 'Ricardo Rei, Craig Stewart, Catarina Farinha, Alon Lavie',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Unbabel/COMET',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
