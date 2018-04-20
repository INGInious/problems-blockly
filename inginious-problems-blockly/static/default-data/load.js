var data={
    "collapse-PID": false,
    "comments-PID": false,
    "disable-PID": false,
    "maxBlocks-PID": "Infinity",
    "trashcan-PID": true,
    "horizontalLayout-PID":false,
    "toolboxPosition-PID": "start",
    "media-PID": "/plugins/blockly/static/blockly/media/",
    "css-PID": true,
    "grid-PID": true,
    "visualPosition-PID": "left",
    "gridSpacing-PID": "20",
    "gridLength-PID": "3",
    "gridColour-PID": "#ccc",
    "gridSnap-PID": true,
    "zoomControls-PID": true,
    "zoomWheel-PID": false,
    "zoomStartScale-PID": "1",
    "zoomMaxScale-PID": "3",
    "zoomMinScale-PID": "0.3",
    "zoomScaleSpeed-PID": "1.2",
    "rtl-PID": false,
    "readOnly-PID":false,
    "oneBasedIndex-PID":true,
    "scrollbars-PID":true,
    "sounds-PID":true,
};

$(function() {
        for(x in data){
            var elem = document.getElementById(x);
            if(elem !== null){
                if(elem.type === "checkbox"){
                    if(data[x]){
                        elem.checked = true;
                    }
                }
                else{
                    elem.value = data[x]
                }
            }
        }
    }
);