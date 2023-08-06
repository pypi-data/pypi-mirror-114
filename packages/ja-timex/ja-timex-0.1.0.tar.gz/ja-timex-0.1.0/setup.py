# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ja_timex', 'ja_timex.pattern']

package_data = \
{'': ['*'], 'ja_timex': ['dictionary/*']}

install_requires = \
['mojimoji>=0.0.11,<0.0.12', 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'ja-timex',
    'version': '0.1.0',
    'description': 'Analyze and parse natural language temporal expression from Japanese sentences',
    'long_description': '![](docs/docs/img/logo_title_wide.png)\n\n# ja-timex\n\n自然言語で書かれた時間情報表現を抽出/規格化するルールベースの解析器\n\n## 概要\n`ja-timex` は、現代日本語で書かれた自然文に含まれる時間情報表現を抽出し`TIMEX3`と呼ばれるアノテーション仕様に変換することで、プログラムが利用できるような形に規格化するルールベースの解析機です。\n\n## インストール\nTBW\n\n## 使い方\nTBW\n\n\n### 参考仕様\n本パッケージは、以下の論文で提案されている`TIMEX3`の仕様を参考に実装しています。\n\n- [1] [小西光, 浅原正幸, & 前川喜久雄. (2013). 『現代日本語書き言葉均衡コーパス』 に対する時間情報アノテーション. 自然言語処理, 20(2), 201-221.](https://www.jstage.jst.go.jp/article/jnlp/20/2/20_201/_article/-char/ja/)\n- [2] [成澤克麻 (2014)「自然言語処理における数量表現の取り扱い」東北大学大学院 修士論文](http://www.cl.ecei.tohoku.ac.jp/publications/2015/mthesis2013_narisawa_submitted.pdf)\n',
    'author': 'Yuki Okuda',
    'author_email': 'y.okuda@dr-ubie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yagays/ja-timex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
