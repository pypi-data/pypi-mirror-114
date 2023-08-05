# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyccup']

package_data = \
{'': ['*']}

install_requires = \
['hy==1.0a2', 'multimethod>=1.5,<2.0', 'toolz>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'hyccup',
    'version': '1.0.0a1',
    'description': 'A port of Clojure Hiccup for Hy',
    'long_description': '# Hyccup\n\n[![Tests](https://github.com/Arkelis/hyccup/actions/workflows/test.yml/badge.svg)](https://github.com/Arkelis/hyccup/actions/workflows/test.yml)\n\nHyccup is a port of [Hiccup](https://github.com/weavejester/hiccup)\nfor [Hy](https://github.com/hylang/hy), a Lisp embed in Python.\n\nIt allows you to represent HTML into data structure and to dump it.\n\n```hy\n=> (import [hyccup.core [html]])\n=> (html [\'div {\'class "my-class" \'id "my-id"} "Hello Hyccup"])\n"<div class=\\"my-class\\" id=\\"my-id\\">Hello Hyccup</div>"\n```\n\n## Differences with Hiccup\n\n### Keywords\n\nAs keywords are not a Python concept and as Hy is very close to Python, they\ncannot be used efficiently. Thus, we rely on strings or symbols instead.\n\nThat is to say, \n\n```hy\n[:div#an-id {:class "a-class"} "some text"]\n```\nmust be changed to\n\n```hy\n["div#an-id" {"class" "a-class"} "some text"] ;; with strings\n[\'div#an-id {\'class "a-class"} "some text"] ;; with symbols\n```\n\n### HTML Options\n\nInstead of passing options in a dictionary as the first argument:\n\n```clj\n(html {:mode "xhtml" :espace-strings? true} [:p "example"])\n```\n\nPass them as keyword arguments (or use unpacking):\n\n```hy\n(html [\'p "example"] :mode "xhtml" :espace-strings True)\n(html [\'p "example"] #** {\'mode "xhtml" \'espace-strings True})\n(html [\'p "example"] (unpack-mapping {\'mode "xhtml" \'espace-strings True}))\n```\n\nNote that the escape flag argument has no `?` suffix in Hyccup.\n\n### Lists\n\nThe following form is valid in Hiccup:\n\n```clj\n(html (list [:p "some text"] [:p "another p"]))\n```\n\nIn Hyccup, just chain the elements or use unpacking (as we already use lists to\nrepresent elements, where Hiccup use Clojure vectors).\n\n```hy\n(html [\'p "some text"] [\'p "another p"]))\n(html #* [[\'p "some text"] [\'p "another p"]]))\n(html (unpack-iterable [[\'p "some text"] [\'p "another p"]])))\n```\n\n### `with-*` macros \n\n`with-base-url` and `with-encoding` are replaced by context managers.\n\nChange\n\n```clj\n=> (with-base-url "/foo/" \n     (to-str (to-uri "/bar")))\n"/foo/bar"\n=> (with-encoding "UTF-8" \n     (url-encode {:iroha "いろは"}))\n"iroha=%E3%81%84%E3%82%8D%E3%81%AF"\n```\n\nTo\n\n```hy\n=> (with [(base-url "/foo/")]\n     (to-str (to-uri "/bar")))\n"/foo/bar"\n=> (with [(encoding "UTF-8")] \n     (url-encode {\'iroha "いろは"}))\n"iroha=%E3%81%84%E3%82%8D%E3%81%AF"\n```\n\n\n### `defhtml` and `defelem`\n\n\n`defhtml` and `defelem` macros from Hiccup is available in two modules:\n\n- `hyccup.defmacros` for using `defhtml` and `defelem` as macros in Hy code:\n\n```hy\n=> (require [hyccup.defmacros [defhtml defelem]])\n=> (defelem link-to [link text]\n...  [\'a {\'href link} text])\n=> (link-to "https://www.pycolore.fr" "Pycolore" )\n[\'a {\'href "https://www.pycolore.fr"} "Pycolore"]\n=> (defhtml linked-section-html [link text content]\n...  [\'section \n...    [\'h1 (link-to link text)]\n...    [\'p content]])\n=> (linked-section-html "https://www.pycolore.fr" "Pycolore" "Lorem Ipsum")\n\'<section>\n   <h1>\n     <a href="https://www.pycolore.fr">Pycolore</a>\n   </h1>\n   <p>\n     Lorem Ipsum\n   </p>\n </section>\'\n```\n\n- `hyccup.defdecos` for using `defhtml` and `defelem`decorators in Python code. See *Python Interop* section.\n\n## Python interop\n\nYou can call Hyccup functions from Python code:\n\n```pycon\n>>> import hy\n>>> from hyccup.core import html\n>>> html(["div", {"class": "my-class", "id": "my-id"}, "Hello Hyccup"])\n\'<div class="my-class" id="my-id">Hello Hyccup</div>\'\n```\n\n`defelem` and `defhtml` macros are available as decorators in Python:\n\n```pycon\n>>> from hyccup.defdecos import defelem, defhtml\n>>> @defhtml # pass output of function to html()\n... @defelem # merge last arg dict with attributes\n... def link_to(link: str, text: str):\n...     return ["a", {"href": link}, text]\n...\n>>> link_to("https://www.pycolore.fr", "Pycolore", {"class": "some-class"})\n\'<a class="some-class" href="https://www.pycolore.fr">Pycolore</a>\'\n```\n\nIt is possible to pass HTML options to `defhtml` decorator\n\n```pycon\n>>> @defhtml(mode="html")\n... def paragraph(content=""):\n...     return ["p", content]\n...\n>>> paragraph()\n\'<p></p>\'\n```\n\n<!-- ## Use Hyccup with web frameworks\n\n### Django\n\n### Flask -->\n',
    'author': 'Guillaume Fayard',
    'author_email': 'guillaume.fayard@pycolore.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Arkelis/hyccup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
