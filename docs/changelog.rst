ChangeLog
=========

First
-----
file track from
static/blockly	eccept blockly.js google/blockly

NB:
static/blocklyfactory can't be tracked because it's custom (from repo fthuin/workspacefactory_bootstrap)

change log: use of audio completely different

* old: Blockly.getMainWorkspace().loadAudio_(...) 
	-> Blockly.getMainWorkspace().getAudioManager().load(...)
* old: Blockly.getMainWorkspace().playAudio(...) 
	-> Blockly.getMainWorkspace().getAudioManager().play(....)
