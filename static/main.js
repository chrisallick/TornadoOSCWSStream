var ws;
setup = function() {
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://localhost:8888/websocket");
    } else {
        ws = new MozWebSocket("ws://localhost:8888/websocket");
    }

    ws.onmessage = function( event ) {
        parseMessage( JSON.parse(event.data) );
    }

    ws.onopen = function( event ) {

    }
}

parseMessage = function( data ) {
    if( data.msg ) {
        $("#msg").html( data.msg )
    }
}

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    setup();
});
