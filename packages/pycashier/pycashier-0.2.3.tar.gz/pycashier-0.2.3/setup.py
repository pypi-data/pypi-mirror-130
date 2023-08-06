# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycashier']

package_data = \
{'': ['*']}

install_requires = \
['pysam>=0.17.0,<0.18.0', 'rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['pycashier = pycashier.pycashier:main']}

setup_kwargs = {
    'name': 'pycashier',
    'version': '0.2.3',
    'description': 'cash in on expressed barcode tags',
    'long_description': "# Cash in on Expressed Barcode Tags (EBTs) from NGS Sequencing Data *with Python*\n\n[Cashier](https://github.com/russelldurrett/cashier) is a tool developed by Russell Durrett for the analysis and extraction of expressed barcode tags.\n\nThis python implementation offers the same flexibility and simple command line operation.\n\nLike it's predecessor it is a wrapper for the tools cutadapt, fastx-toolkit, and starcode.\n\n### Dependencies\n- cutadapt (sequence extraction)\n- starcode (sequence clustering)\n- fastx-toolkit (PHred score filtering)\n- pear (paired end read merging)\n- pysam (sam file convertion to fastq)\n\n## Recommended Installation Procedure\nIt's recommended to use [conda](https://docs.conda.io/en/latest/) to install and manage the dependencies for this package\n\n```bash\nconda env create -f https://raw.githubusercontent.com/brocklab/pycashier/main/environment.yml # or mamba env create -f ....\nconda activate cashierenv\npycashier --help\n```\n\nAdditionally you may install with pip. Though it will be up to you to ensure all the non-python dependencies are on the path and installed correctly.\n\n```bash\npip install pycashier\n```\n\n## Usage\n\nPycashier has one required argument which is the directory containing the fastq or sam files you wish to process.\n\n```bash\nconda activate cashierenv\npycashier ./fastqs\n```\nFor additional parameters see `pycashier -h`.\n\nAs the files are processed two additional directories will be created `pipeline` and `outs`.\n\nCurrently all intermediary files generated as a result of the program will be found in `pipeline`.\n\nWhile the final processed files will be found within the `outs` directory.\n\n## Merging Files\n\nPycashier can now take paired end reads and perform a merging of the reads to produce a fastq which can then be used with cashier's default feature.\n```bash\npycashier ./fastqs -m\n```\n\n## Processing Barcodes from 10X bam files\n\nPycashier can also extract gRNA barcodes along with 10X cell and umi barcodes.\n\nFirstly we are only interested in the unmapped reads. From the cellranger bam output you would obtain these reads using samtools.\n\n```\nsamtools view -f 4 possorted_genome_bam.bam > unmapped.sam\n```\nThen similar to normal barcode extraction you can pass a directory of these unmapped sam files to pycashier and extract barcodes. You can also still specify extraction parameters that will be passed to cutadapt as usual.\n\n*Note*: The default parameters passed to cutadapt are unlinked adapters and minimum barcode length of 10 bp.\n\n```\npycashier ./unmapped_sams -sc\n```\nWhen finished the `outs` directory will have a `.tsv` containing the following columns: Illumina Read Info, UMI Barcode, Cell Barcode, gRNA Barcode\n\n\n## Usage notes\nPycashier will **NOT** overwrite intermediary files. If there is an issue in the process, please delete either the pipeline directory or the requisite intermediary files for the sample you wish to reprocess. This will allow the user to place new fastqs within the source directory or a project folder without reprocessing all samples each time.\n- Currently, pycashier expects to find `.fastq.gz` files when merging and `.fastq` files when extracting barcodes. This behavior may change in the future.\n- If there are reads from multiple lanes they should first be concatenated with `cat sample*R1*.fastq.gz > sample.R1.fastq.gz`\n- Naming conventions:\n    - Sample names are extracted from files using the first string delimited with a period. Please take this into account when naming sam or fastq files.\n    - Each processing step will append information to the input file name to indicate changes, again delimited with periods.\n",
    'author': 'Daylin Morgan',
    'author_email': 'daylinmorgan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brocklab/pycashier/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
