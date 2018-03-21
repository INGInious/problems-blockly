/**
 * Init a blockly template
 * @param well: the DOM element containing the input fields
 * @param pid
 * @param problem
 */
function studio_init_template_blockly(well, pid, problem) {
    var row, new_row_content;
    var val = "";

    var toolboxEditor = registerCodeEditor($('#toolbox-' + pid)[0], 'xml', 10);
    toolboxEditor.setValue("toolbox" in problem ? problem.toolbox : "<xml></xml>");

    var workspaceEditor = registerCodeEditor($('#workspace-' + pid)[0], 'xml', 10);
    workspaceEditor.setValue("workspace" in problem ? problem.workspace : "<xml></xml>");

    var options = "options" in problem ? problem.options : {};

    $("#collapse-" + pid).prop('checked', "collapse" in options ? options.collapse : false);
    $("#comments-" + pid).prop('checked', "comments" in options ? options.comments : false);
    $("#disable-" + pid).prop('checked', "disable" in options ? options.disable : false);
    $("#maxBlocks-" + pid).val("maxBlocks" in options ? options.maxBlocks : "Infinity");
    $("#trashcan-" + pid).prop('checked', "trashcan" in options ? options.trashcan : true);
    $("#horizontalLayout-" + pid).prop('checked', "horizontalLayout" in options ? options.horizontalLayout : false);

    if ("toolboxPosition" in options && (options.toolboxPosition === "start" || options.toolboxPosition === "end")) {
        $("#toolboxPosition-" + pid).val(options.toolboxPosition);
    } else { // assign default value
        $("#toolboxPosition-" + pid).val("start");
    }

    $("#css-" + pid).prop('checked', "css" in options ? options.css : true);
    $("#rtl-" + pid).prop('checked', "rtl" in options ? options.rtl : false);
    $("#scrollbars-" + pid).prop('checked', "scrollbars" in options ? options.scrollbars : true);
    $("#sounds-" + pid).prop('checked', "sounds" in options ? options.sounds : true);
    $("#media-" + pid).val("media" in options ? options.media : "plugins/blockly/static/blockly/media/");
    $("#oneBasedIndex-" + pid).prop('checked', "oneBasedIndex" in options ? options.oneBasedIndex : true);
    $("#readOnly-" + pid).prop('checked', "readOnly" in options ? options.readOnly : false);

    var visualOptions;

    if ("visual" in options) {
        row = $("#subproblem_blockly_visual").html();
        new_row_content = row.replace(/PID/g, pid);
        $('#visual-' + pid).parent().parent().append(new_row_content);
        visualOptions = options.visual;
        $("#visual-" + pid).prop('checked', true);
    } else {
        visualOptions = {};
        $("#visual-" + pid).prop('checked', false);
    }

    if (visualOptions === true) visualOptions = {position : "left"};
    $("#visualPosition-" + pid).val("position" in visualOptions ? visualOptions.position : "left");

    $('#visual-' + pid).change(function() {
        if ($(this).is(":checked")) {
            var row = $("#subproblem_blockly_visual").html();
            var new_row_content = row.replace(/PID/g, pid);
            $(this).parent().parent().append(new_row_content);
        } else {
            $(this).parent().parent().html($(this).parent().detach());
        }
    });

    var gridOptions;

    if ("grid" in options) {
        // If grid is set, display the grid options
        row = $("#subproblem_blockly_grid").html();
        new_row_content = row.replace(/PID/g, pid);
        $('#grid-' + pid).parent().parent().parent().append(new_row_content);
        gridOptions = options.grid;
        $("#grid-" + pid).prop('checked', true);
    } else {
        gridOptions = {};
        $("#grid-" + pid).prop('checked', false);
    }

    $("#gridSpacing-" + pid).val("spacing" in gridOptions ? gridOptions.spacing : "20");
    $("#gridLength-" + pid).val("length" in gridOptions ? gridOptions.length : "3");
    $("#gridColour-" + pid).val("colour" in gridOptions ? gridOptions.colour : "#ccc");
    $("#gridSnap-" + pid).prop('checked', "snap" in gridOptions ? gridOptions.snap : true);

    $('#grid-' + pid).change(function() {
        if ($(this).is(":checked")) {
            var row = $("#subproblem_blockly_grid").html();
            var new_row_content = row.replace(/PID/g, pid);
            $(this).parent().parent().parent().append(new_row_content);
        } else {
            $(this).parent().parent().parent().html($(this).parent().parent().detach());
        }
    });

    var zoomOptions;
    if ("zoom" in options) {
        var row = $("#subproblem_blockly_zoom").html();
        var new_row_content = row.replace(/PID/g, pid);
        $('#zoom-' + pid).parent().parent().parent().append(new_row_content);
        $("#zoom-" + pid).prop('checked', true);
        zoomOptions = options.zoom;
    } else {
        zoomOptions = {};
        $("#zoom-" + pid).prop('checked', false);
    }

    $("#zoomControls-" + pid).prop('checked', "controls" in zoomOptions ? zoomOptions.controls : true);
    $("#zoomWheel-" + pid).prop('checked', "wheel" in zoomOptions ? zoomOptions.wheel : false);
    $("#zoomStartScale-" + pid).val("startScale" in zoomOptions ? zoomOptions.startScale : "1.0");
    $("#zoomMaxScale-" + pid).val("maxScale" in zoomOptions ? zoomOptions.maxScale :"3.0");
    $("#zoomMinScale-" + pid).val("minScale" in zoomOptions ? zoomOptions.minScale : "0.3");
    $("#zoomScaleSpeed-" + pid).val("scaleSpeed" in zoomOptions ? zoomOptions.scaleSpeed : "1.2");

    $('#zoom-' + pid).change(function() {
        if ($(this).is(":checked")) {
            var row = $("#subproblem_blockly_zoom").html();
            var new_row_content = row.replace(/PID/g, pid);
            $(this).parent().parent().parent().append(new_row_content);
        } else {
            $(this).parent().parent().parent().html($(this).parent().parent().detach());
        }
    });

    if ("files" in problem) {
        jQuery.each(problem["files"], function(index, elem)
        {
            studio_create_blockly_js_files(pid, elem);
        });
    }
    if ("blocks_files" in problem) {
        jQuery.each(problem["blocks_files"], function(index, elem)
        {
            studio_create_blockly_blocks_files(pid, elem);
        });
    }

    var factoryController;
    $('#blockFactoryModal').on('shown.bs.modal', function() {
        // FIXME Next line is a fix, please monitor https://github.com/google/blockly/issues/56
        $(document).off('focusin.modal');

        $("#blockFactoryModalBody").html($("#subproblem_blockly_factory").detach());

        var basicToolbox = Toolbox.FULL;
        var toolbox = $("#toolbox-" + pid).text();
        var workspaceBlocks = $("#workspace-" + pid).text();

        factoryController = new FactoryController('blocklyFactory', basicToolbox, workspaceBlocks, problem["options"], pid);
        var preview = new Preview(factoryController);
        factoryController.setPreview(preview);
        factoryController.injectWorkspaces();
    });

    $('#blockFactoryModal').on('hidden.bs.modal', function() {
        // If you want this behavior to be BEFORE the visual part, use hide.bs.modal, if after use hidden.bs.modal
        // When the modal is closed, the workspace (from the initial page must be updated)
        factoryController.dispose();
    });

}

/**
 * Create a new input for the name of a file
 * @param pid
 * @param filename
 */
function studio_create_blockly_js_files(pid, filename)
{
    var index = 0;
    while($('#file-' + pid + '-' + index).length !== 0)
        index++;

    var row = $("#subproblem_blockly_files").html();
    var new_row_content = row.replace(/PID/g, pid).replace(/INDEX/g, index);
    var new_row = $("<div></div>").attr('id', 'blocklyFiles-' + index + '-' + pid).html(new_row_content);
    $("#javascript_files-" + pid).append(new_row);

    if (jQuery.type(filename) === "string") {
        $("#file-" + pid + "-" + index).val(filename);
        var script = $("<script>");
        script.prop("charset", "utf-8");
        script.prop("src", $("#switch").attr("href") + "/" + filename);
        $("#collapse_" + pid).append(script);
    } else {
        $("#file-" + pid + "-" + index).val("");
    }
}

function studio_create_blockly_blocks_files(pid, filename)
{
    var index = 0;
    while($('#file-' + pid + '-' + index).length !== 0)
        index++;

    var row = $("#subproblem_blocks_files").html();
    var new_row_content = row.replace(/PID/g, pid).replace(/INDEX/g, index);
    var new_row = $("<div></div>").attr('id', 'blocklyFiles-' + index + '-' + pid).html(new_row_content);
    $("#javascript_blocks_files-" + pid).append(new_row);

    if (jQuery.type(filename) === "string") {
        $("#file-" + pid + "-" + index).val(filename);
        var script = $("<script>");
        script.prop("charset", "utf-8");
        script.prop("src", $("#switch").attr("href") + "/" + filename);
        $("#collapse_" + pid).append(script);
    } else {
        $("#file-" + pid + "-" + index).val("");
    }
}