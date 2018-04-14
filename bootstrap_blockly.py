#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import os
import subprocess
import shlex


p = subprocess.Popen(shlex.split("git submodule update --remote blockly"),stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
print(p.communicate()[0].decode('utf-8'))

submodule_blockly = "blockly"
problems_blockly = "inginious-problems-blockly/static/blockly"

for file in os.listdir(submodule_blockly):
	if file.endswith("_compressed.js") and not file.endswith("_accessible_compressed.js"):
		shutil.copy2(submodule_blockly + "/" + file, problems_blockly + "/" + file)
		print(file + "copied")

shutil.rmtree(problems_blockly + "/media")
shutil.copytree(submodule_blockly + "/media", problems_blockly + "/media")
print("media/ copied")

shutil.rmtree(problems_blockly + "/msg")
shutil.copytree(submodule_blockly + "/msg", problems_blockly + "/msg")
print("msg/ copied")
