# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['super_image',
 'super_image.data',
 'super_image.models',
 'super_image.models.a2n',
 'super_image.models.edsr',
 'super_image.models.masa',
 'super_image.models.msrn',
 'super_image.models.pan',
 'super_image.utils']

package_data = \
{'': ['*']}

install_requires = \
['h5py==3.1.0',
 'huggingface-hub>=0.0.13,<0.0.14',
 'opencv-python==4.5.2.54',
 'torch==1.9.0',
 'torchvision==0.10.0',
 'tqdm==4.61.2']

entry_points = \
{'console_scripts': ['super-image = super_image.cli:main']}

setup_kwargs = {
    'name': 'super-image',
    'version': '0.1.2',
    'description': 'State-of-the-art image super resolution models for PyTorch.',
    'long_description': '<h1 align="center">super-image</h1>\n\n<p align="center">\n    <a href="https://eugenesiow.github.io/super-image/">\n        <img alt="documentation" src="https://img.shields.io/badge/docs-mkdocs-blue.svg?style=flat">\n    </a>\n    <a href="https://github.com/eugenesiow/super-image/blob/main/LICENSE">\n\t\t<img alt="GitHub" src="https://img.shields.io/github/license/eugenesiow/super-image.svg?color=blue">\n\t</a>\n    <a href="https://pypi.org/project/super-image/">\n        <img alt="pypi version" src="https://img.shields.io/pypi/v/super-image.svg">\n    </a>\n</p>\n\n<h3 align="center">\n    <p>State-of-the-art image super resolution models for PyTorch.</p>\n</h3>\n\n\n## Requirements\n\nsuper-image requires Python 3.6 or above.\n\n## Installation\n\nWith `pip`:\n```bash\npip install super-image\n```\n\n## Quick Start\n\nQuickly utilise pre-trained models for upscaling your images 2x, 3x and 4x. See the full list of models [below](#pre-trained-models).\n\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/eugenesiow/super-image/blob/master/notebooks/Upscale_Images_with_Pretrained_super_image_Models.ipynb "Open in Colab")\n\n```python\nfrom super_image import EdsrModel, ImageLoader\nfrom PIL import Image\nimport requests\n\nurl = \'https://paperswithcode.com/media/datasets/Set5-0000002728-07a9793f_zA3bDjj.jpg\'\nimage = Image.open(requests.get(url, stream=True).raw)\n\nmodel = EdsrModel.from_pretrained(\'eugenesiow/edsr-base\', scale=2)\ninputs = ImageLoader.load_image(image)\npreds = model(inputs)\n\nImageLoader.save_image(preds, \'./scaled_2x.png\')\nImageLoader.save_compare(inputs, preds, \'./scaled_2x_compare.png\')\n```\n\n## Pre-trained Models\nPre-trained models are available at various scales and hosted at the awesome [`huggingface_hub`](https://huggingface.co/models?filter=super-image). By default the models were pretrained on [DIV2K](https://huggingface.co/datasets/eugenesiow/Div2k), a dataset of 800 high-quality (2K resolution) images for training, augmented to 4000 images and uses a dev set of 100 validation images (images numbered 801 to 900). \n\nThe leaderboard below shows the [PSNR](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio#Quality_estimation_with_PSNR) / [SSIM](https://en.wikipedia.org/wiki/Structural_similarity#Algorithm) metrics for each model at various scales on various test sets ([Set5](https://huggingface.co/datasets/eugenesiow/Set5), [Set14](https://sites.google.com/site/romanzeyde/research-interests), [BSD100](https://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/), [Urban100](https://sites.google.com/site/jbhuang0604/publications/struct_sr)). The **higher the better**. \nAll training was to 1000 epochs (some publications, like a2n, train to >1000 epochs in their experiments). \n\n### Scale x2\n\n|Rank   |Model  \t                                                |Params         |Set5  \t            |Set14  \t        |BSD100  \t        |Urban100  \t        |\n|---    |---\t                                                    |---            |---                |---\t            |---\t            |---\t            |\n|1      |[msrn-bam](https://huggingface.co/eugenesiow/msrn-bam)  \t|5.9m           |**38.02/0.9607**   |**33.63/0.9177**  \t|32.20/0.8998  \t    |**32.08/0.9276**   |\n|2      |[edsr-base](https://huggingface.co/eugenesiow/edsr-base)  \t|1.5m           |**38.02/0.9607**   |33.57/0.9172       |**32.21/0.8999**   |32.04/0.9276       |\n|3      |[a2n](https://huggingface.co/eugenesiow/a2n)   \t        |1.0m           |37.87/0.9602       |33.45/0.9162       |32.11/0.8987       |31.71/0.9240       |\n\n### Scale x3\n\n|Rank   |Model  \t                                                |Params         |Set5  \t            |Set14  \t        |BSD100  \t        |Urban100  \t        |\n|---    |---\t                                                    |---            |---                |---\t            |---\t            |---\t            |\n|1      |[msrn-bam](https://huggingface.co/eugenesiow/msrn-bam)  \t|5.9m           |**35.16/0.9410**   |**30.97/0.8574**  \t|**29.67/0.8209**   |**29.31/0.8737**   |\n|2      |[edsr-base](https://huggingface.co/eugenesiow/edsr-base)  \t|1.5m           |35.04/0.9403       |30.93/0.8567       |29.65/0.8204       |29.23/0.8723       |\n\n### Scale x4\n\n|Rank   |Model  \t                                                |Params         |Set5  \t            |Set14  \t        |BSD100  \t        |Urban100  \t        |\n|---    |---\t                                                    |---            |---                |---\t            |---\t            |---\t            |\n|1      |[msrn-bam](https://huggingface.co/eugenesiow/msrn-bam)  \t|5.9m           |**32.26/0.8955**   |28.66/0.7829       |27.61/0.7369       |26.10/0.7857       |\n|2      |[msrn](https://huggingface.co/eugenesiow/msrn)             |6.1m           |32.19/0.8951       |**28.67/0.7833**   |**27.63/0.7374**   |**26.12/0.7866**   |\n|3      |[edsr-base](https://huggingface.co/eugenesiow/edsr-base)  \t|1.5m           |32.12/0.8947       |28.60/0.7815       |27.61/0.7363       |26.02/0.7832       |\n|4      |[a2n](https://huggingface.co/eugenesiow/a2n)               |1.0m           |32.07/0.8933       |28.56/0.7801       |27.54/0.7342       |25.89/0.7787       |',
    'author': 'Eugene Siow',
    'author_email': 'kyo116@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eugenesiow/super-image',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
