# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacypdfreader']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20211012,<20211013',
 'rich>=10.15.2,<11.0.0',
 'spacy>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'spacypdfreader',
    'version': '0.1.1',
    'description': 'A PDF to text extraction pipeline component for spaCy.',
    'long_description': '# spacypdfreader\n\nExtract text from PDFs using spaCy and capture the page number as a spaCy extension.\n\n**Links**\n\n- [GitHub](https://github.com/SamEdwardes/spaCyPDFreader)\n- [PyPi](https://pypi.org/project/spacypdfreader/)\n\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Implementation Notes](#implementation-notes)\n- [API Reference](#api-reference)\n\n## Installation\n\n```bash\npip install spacypdfreader\n```\n\n## Usage\n\n```python\n>>> import spacy\n>>> from spacypdfreader import pdf_reader\n>>>\n>>> nlp = spacy.load("en_core_web_sm")\n>>> doc = pdf_reader("tests/data/test_pdf_01.pdf", nlp)\nExtracting text from 4 pdf pages... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00\n```\n\nEach token will now have an additional extension `._.page_number` that indcates the pdf page number the token came from.\n\n```python\n>>> [print(f"Token: `{token}`, page number  {token._.page_number}") for token in doc[0:3]]\nToken: `Test`, page number  1\nToken: `PDF`, page number  1\nToken: `01`, page number  1\n[None, None, None]\n```\n\n## Implementation Notes\n\nspaCyPDFreader behaves a litptle bit different than your typical [spaCy custom component](https://spacy.io/usage/processing-pipelines#custom-components). Typically a spaCy component should receive and return a `spacy.tokens.Doc` object.\n\nspaCyPDFreader breaks this convention because the text must first be extracted from the PDF. Instead `pdf_reader` takes a path to a PDF file and a `spacy.Language` object as parameters and returns a `spacy.tokens.Doc` object. This allows users an easy way to extract text from PDF files while still allowing them use and customize all of the features spacy has to offer by allowing you to pass in the `spacy.Language` object.\n\nExample of a "traditional" spaCy pipeline component [negspaCy](https://spacy.io/universe/project/negspacy):\n\n```python\n>>> import spacy\n>>> from negspacy.negation import Negex\n>>> \n>>> nlp = spacy.load("en_core_web_sm")\n>>> nlp.add_pipe("negex", config={"ent_types":["PERSON","ORG"]})\n>>> \n>>> doc = nlp("She does not like Steve Jobs but likes Apple products.")\n```\n\nExample of `spaCyPDFreader` usage:\n\n```python\n>>> import spacy\n>>> from spacypdfreader import pdf_reader\n>>>\n>>> nlp = spacy.load("en_core_web_sm")\n>>> doc = pdf_reader("tests/data/test_pdf_01.pdf", nlp)\nExtracting text from 4 pdf pages... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00\n```\n\nNote that the `nlp.add_pipe` is not used by spaCyPDFreader.\n\n## API Reference\n\n### Functions\n\n### `spacypdfreader.pdf_reader`\n\nExtract text from PDF files directly into a `spacy.Doc` object while capturing the page number of each token.\n\n| Name        | Type               | Description                                                                                |\n| ------------- | -------------------- | -------------------------------------------------------------------------------------------- |\n| `pdf_path`  | `str`              | Path to a PDF file.                                                                        |\n| `nlp`       | `spacy.Language`   | A spaCy Language object with a loaded pipeline. For example`spacy.load("en_core_web_sm")`. |\n| **RETURNS** | `spacy.tokens.Doc` | A spacy Doc object with the custom extension`._.page_number`.                              |\n\n**Example**\n\n```python\n>>> import spacy\n>>> from spacypdfreader import pdf_reader\n>>>\n>>> nlp = spacy.load("en_core_web_sm")\n>>> doc = pdf_reader("tests/data/test_pdf_01.pdf", nlp)\nExtracting text from 4 pdf pages... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00\n>>> [print(f"Token: `{token}`, page number  {token._.page_number}") for token in doc[0:3]]\nToken: `Test`, page number  1\nToken: `PDF`, page number  1\nToken: `01`, page number  1\n[None, None, None]\n```\n\n### Extensions\n\nWhen using `spacypdfreader.pdf_reader` a `spacy.tokens.Doc` object with custom extensions is returned.\n\n| Extension   | Type   | Description   | Default   |\n| ------ | ------ | ------ | ------ |\n| token._.page_number |  int      | The PDF page number in which the token was extracted from. The first page is `1`.      |  `None`      |',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/spaCyPDFreader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
