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

function load_feedback_blockly(key, content){
    //This part is a temporary workaround
    if (typeof Maze !== "undefined" && typeof Maze.reset !== "undefined" && content[0] !== "success") {    
        var test = $('<div>');
        test.html(content[1]);
        var parsed = jQuery.parseJSON(test.text());
        Maze.reload_maze(parsed );
    }
}

function load_webstorage_blockly(courseid,problemid){
    try {
      var wsp = Blockly.getMainWorkspace();
      var name = courseid+"/"+problemid;
      var code = localStorage[name];
      var dom = Blockly.Xml.textToDom(code);
      Blockly.Xml.domToWorkspace(dom,wsp);
    }
    catch(error) {
      console.error(error);
      // expected output: ReferenceError: nonExistentFunction is not defined
      // Note - error messages will vary depending on browser
    }
}

function save_webstorage_blockly(courseid,problemid){
    try
    {
      var wsp = Blockly.getMainWorkspace();
      var dom =  Blockly.Xml.workspaceToDom(wsp);
      var code = Blockly.Xml.domToText(dom);
      var name = courseid+"/"+problemid;
      localStorage.setItem(name, code);

    }
    catch(error) {
      console.error(error);
      // expected output: ReferenceError: nonExistentFunction is not defined
      // Note - error messages will vary depending on browser
    }

}
