ChangeLog
=========

2018 Apr 14
-----------
commit ec06d866b7571728cce9ced10752f54583a8d73a


Use of audio completely different.

* old: Blockly.getMainWorkspace().loadAudio_(...) 
	-> Blockly.getMainWorkspace().getAudioManager().load(...)
* old: Blockly.getMainWorkspace().playAudio(...) 
	-> Blockly.getMainWorkspace().getAudioManager().play(....)
