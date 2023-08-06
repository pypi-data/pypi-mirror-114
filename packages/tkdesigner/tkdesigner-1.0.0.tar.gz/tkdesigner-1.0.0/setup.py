# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tkdesigner', 'tkdesigner.figma']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==3.0.1', 'requests==2.25.1', 'urllib3==1.26.4']

entry_points = \
{'console_scripts': ['tkdesigner = tkdesigner.cli:main']}

setup_kwargs = {
    'name': 'tkdesigner',
    'version': '1.0.0',
    'description': 'CLI Package for Tkinter-Designer',
    'long_description': '<p align="center">\n  <img width="200" src="https://user-images.githubusercontent.com/42001064/120057695-b1f6c680-c062-11eb-96d5-2c43d05f9018.png" alt="logo">\n  <h1 align="center" style="margin: 0 auto 0 auto;">Tkinter Designer</h1>\n  <h5 align="center" style="margin: 0 auto 0 auto;">Automate Tkinter GUI Creation</h5>\n  </p>\n\n  <p align="center">\n    <img src="https://img.shields.io/github/last-commit/ParthJadhav/Tkinter-Designer">\n    <img src="https://img.shields.io/github/contributors/ParthJadhav/Tkinter-Designer">\n    <img src="https://img.shields.io/github/issues/ParthJadhav/Tkinter-Designer?label=issues">\n    <img src="https://img.shields.io/github/stars/ParthJadhav/Tkinter-Designer">\n  </p>\n\n  <br>\n\n## Translations\n- [简体中文](/docs/README.zh-CN.md)\n- [Français](/docs/README.fr-FR.md)\n- [ગુજરાતી](/docs/README.gu-GU.md)\n\n___ \n\n## 💡 Introduction\nTkinter Designer was created to speed up the GUI development process in Python. It uses the well-known design software [Figma](https://www.figma.com/) to make creating beautiful Tkinter GUIs in Python a piece of cake 🍰.\n\nTkinter Designer uses the Figma API to analyse a design file and create the respective code and files needed for the GUI. Even Tkinter Designer\'s GUI is created using Tkinter Designer.\n\n<img width="500" alt="Tkinter Designer GUI" src="https://user-images.githubusercontent.com/42001064/119863796-92af4a80-bf37-11eb-9f6c-61b1ab99b039.png">\n\n## ☄️  Advantages of Tkinter Designer\n1. Drag and drop interfaces\n2. Significantly faster than creating code manually\n3. Ability to create more beautiful interfaces\n\n___\n\n## 🦋 Supporting Tkinter Designer\n\nLife without coffee is like something without something … sorry, I haven’t had any coffee yet. \n\n<a href="https://www.buymeacoffee.com/Parthjadhav" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="217px" ></a> \n\n\n## ⚡️ Installing & Using Tkinter Designer\n\nThe instructions contain all the information about installing and using Tkinter Designer, along with information for troubleshooting and reporting issues. There is also a video.\n\n### [Read the Instructions](/docs/instructions.md)\n### [Watch the Video](https://youtu.be/mFjE2-rbpm8)  \n\n___\n<br>\n\n## 🔵 Join Official Tkinter Designer\'s Discord server\n\nClick the button below to join the discord server and take part in discussions. \n\n<a href="https://discord.gg/QfE5jMXxJv" target="_blank"><img src="https://user-images.githubusercontent.com/42001064/126635148-9a736436-5a6d-4298-8d8e-acda11aec74c.png" alt="Join Discord Server" width="217px" ></a> \n\n\n## ✅  Importance of Naming (mentioned in the [video](https://youtu.be/mFjE2-rbpm8) and [instructions](/docs/instructions.md))\n\nTkinter Designer heavily depends on names of the elements to convert it to code. See the naming guide [here](/docs/instructions.md#2-element-guide).\n___\n<br>\n\n## 📐 How it Works\nThe only thing the user needs to do is design an interface with Figma, and then paste the Figma file URL and API token into Tkinter Designer.\n\nTkinter Designer will automatically generate all the code and images required to create the GUI in Tkinter.\n\n<img width="467" alt="How it Works" src="https://user-images.githubusercontent.com/42001064/119832620-fb88c980-bf1b-11eb-8e9b-4affe7b92ba2.jpg">\n\n___\n<br>\n\n## 🎯 Examples\nThe possibilities are endless with Tkinter Designer, but here are a couple of GUIs that can be perfectly replicated in Tkinter.\n\n<sup>The following are not my creations.</sup>\n\n### Registration Page\n<img width="467" alt="Example 1" src="https://user-images.githubusercontent.com/42001064/119250338-1f1adf80-bbbd-11eb-8ee1-72028a4e7a7f.png">\n\n### Branding Page\n<img width="467" alt="Example 2" src="https://user-images.githubusercontent.com/42001064/119250668-496d9c80-bbbf-11eb-886b-cb1e75da18df.png">\n\n### Frame Recorder [(More Info)](https://github.com/mehmet-mert/FrameRecorder)\n<img width="467" alt="Example 3" src="https://user-images.githubusercontent.com/42001064/119834287-71d9fb80-bf1d-11eb-9acf-e7bfc8cc4d9e.png">\n\n### WhatBulk  [(More Info)](https://www.instagram.com/p/CQUmKckFBbT/?utm_medium=copy_link)\n<img width="467" alt="Example 3" src="https://user-images.githubusercontent.com/42001064/122562284-87e06500-d060-11eb-8257-55f3b9dbecf0.PNG">\n\n\n## 🔥 Showcase\nIf your app was made with Tkinter Designer, let me know. It will be helpful for others to see more examples!  \n(See: [Contact Me](#-contact-me)) or use [Show and Tell](https://github.com/ParthJadhav/Tkinter-Designer/discussions/categories/show-and-tell) section in Discussions.\n\n___\n<br>\n \n\n## 📝 Contact Me\n\nIf you want to contact me, you can reach me at Jadhavparth99@gmail.com\n\n___\n<br>\n\n## 📄 License\n<!--- If you\'re not sure which open license to use see https://choosealicense.com/--->\n\nTkinter Designer is licensed under the BSD 3-Clause "New" or "Revised" License.  \n[View Here.](https://github.com/ParthJadhav/Tkinter-Designer/blob/master/LICENSE)\n\n| Permissions | Restrictions | Conditions\n| --- | --- | --- \n&check; Commercial Use | &times; Liability | &#x1f6c8; License and Copyright Notice\n&check; Modification   | &times; Warranty\n&check; Distribution  \n&check; Private Use\n',
    'author': 'ParthJadhav',
    'author_email': 'jadhavparth99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ParthJadhav/Tkinter-Designer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
