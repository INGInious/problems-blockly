Installation and upgrade
========================

Installing
----------

    pip3 install git+https://github.com/UCL-INGI/INGInious-problems-blockly


Activating
----------

In your ``configuration.yaml`` file, add the following plugin entry:

    plugins:
      \- plugin_module: "inginious-problems-blockly"



Updating
--------

Some files can be automaticlly update via the google submodule. 
You just have to run the ``bootstrap_blockly.py`` script.

Running the script update all the file in ``static/blockly`` except ``blockly.js``

**Be carefull about dependecies! Update the changelog with modification to do.**

NB:
static/blocklyfactory can't be tracked because it's custom (from  this `repo <https://github.com/fthuin/workspacefactory_bootstrap>`_)
