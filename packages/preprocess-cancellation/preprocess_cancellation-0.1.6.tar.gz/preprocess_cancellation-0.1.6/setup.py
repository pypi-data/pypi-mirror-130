# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['preprocess_cancellation']
extras_require = \
{'shapely': ['shapely']}

entry_points = \
{'console_scripts': ['preprocess_cancellation = preprocess_cancellation:_main']}

setup_kwargs = {
    'name': 'preprocess-cancellation',
    'version': '0.1.6',
    'description': 'GCode processor to add klipper cancel-object markers',
    'long_description': 'Klipper GCode Preprocessor for Object Cancellation\n==================================================\n\nThis preprocessor modifies GCode files to add klipper\'s exclude object gcode.\n\nThe following slicers are supported:\n\n* SuperSlicer\n* PrusaSlicer\n* Slic3r\n* Cura\n* IdeaMaker\n\n## Installation and usage\n\n### SuperSlicer, PrusaSlicer, and Slic3r\n\nDownload the provided binary for your platform, and place it in with in your slicer\'s folder.\n\nIn your Print Settings, under Output Options, add `preprocessor.exe;` to the "Post-Processing Scripts".\nFor mac or linux, you should just use `preprocessor;`\n\nThen, all generated gcode should be automatically processed and rewritten to support cancellation.\n\n### G-Codes for Object Cancelation\n\nThere are 3 gcodes inserted in the files automatically, and 4 more used to control the \nobject cancellation.\n\n`DEFINE_OBJECT NAME=<object name> [CENTER=x,y] [POLYGON=[[x,y],...]]`\n\nThe NAME must be unique and consistent throughout the file. CENTER is the center location \nfor the mesh, used to show on interfaces where and object being canceled is on the bed. \nPOLYGON is a series of points, used to represent the bounds of the object. It can be just \na bounding box, a simplified outline, or another useful shape.\n\n`START_CURRENT_OBJECT NAME=<object name>` and `END_CURRENT_OBJECT [NAME=<object name>]`\n\nThe beginning and end markers for the gcode for a single object. When an object is excluded, \nanything between these markers is ignored.\n\n`LIST_OBJECTS`\n`LIST_EXCLUDED_OBJECTS`\n`EXCLUDE_OBJECT NAME=<object name>`\n`REMOVE_ALL_EXCLUDED`\n\nThese gcode are used by the user to locate objects, and control which are canceled. These \nare mostly utility, to be functional without the need for a full frontend for the printer.\n\n### Known Limitations\n\nCura and Ideamaker sliced files have all support material as a single non-mesh entity.\nThis means that when canceling an object, it\'s support will still print. Including\nsupport that is inside or built onto the canceled mesh. The Slic3r family (including\nPrusaSlicer and SuperSlicer) treat support as part of the individual mesh\'s object,\nso canceling a mesh cancels it\'s support as well.\n\n### How does it work\n\nThis looks for known markers inside the GCode, specific to each slicer. It uses those\nto figure out the printing object\'s name, and track\'s all extrusion moves within it\'s \nprint movements. Those are used to calculate a minimal bounding box for each mesh. \nA series of `DEFINE_OBJECT` gcodes are placed in a header, including the bounding boxes\nand objects centers. Then, these markers are used to place `START_CURRENT_OBJECT` and \n`END_CURRENT_OBJECT` gcodes in the file surrounding each set of extrusions for that object.\n',
    'author': 'Franklyn Tackitt',
    'author_email': 'im@frank.af',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kageurufu/cancelobject-preprocessor',
    'py_modules': modules,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0',
}


setup(**setup_kwargs)
