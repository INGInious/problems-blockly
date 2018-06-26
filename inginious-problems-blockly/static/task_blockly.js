function load_input_blockly(submissionid, key, input) {

    var codearea = $("form#task textarea#codeArea[name='" + key + "']");
    if(codearea.attr('type') == "hidden") //do not try to change @action
        return;

    if (key in input) {
        codearea.prop('value', input[key]);
    }

    var blocklydiv = $("form#task div#blocklyDiv[data-pid='" + key + "']");
    if(blocklydiv.attr('type') == "hidden") //do not try to change @action
        return;

    if ("blockly" in input) {
        Blockly.getMainWorkspace().clear();
        var xml = Blockly.Xml.textToDom(input["blockly"]);
        Blockly.Xml.domToWorkspace(xml, Blockly.getMainWorkspace());
    }

    var blocklyxmlarea = $('#blocklyXmlArea');
    if(blocklyxmlarea.attr('type') == "hidden") //do not try to change @action
        return;

    if ("blockly" in input) {
        blocklyxmlarea.prop('value', input["blockly"]);
    }

}