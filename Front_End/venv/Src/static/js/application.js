// // Client Side Javascript to receive numbers.
// $(document).ready(function() {
//   // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
//   var socket = io.connect(
//     "http://" + document.domain + ":" + location.port + "/test"
//   );
//   // this is a callback that triggers when the "my response" event is emitted by the server.
//   socket.on("my response", function(msg) {
//     $("#log").append("<p>Received: " + msg.data + "</p>");
//   });
//   //example of triggering an event on click of a form submit button
//   $("form#emit").submit(function(event) {
//     socket.emit("my event", { data: $("#emit_data").val() });
//     return false;
//   });
// });

$(document).ready(function() {
  //connect to the socket server.
  var socket = io.connect(
    "http://" + document.domain + ":" + location.port + "/test"
  );
  var numbers_received = [];

  //receive details from server
  socket.on("newnumber", function(msg) {
    console.log("Received number" + msg.number);
    //maintain a list of ten numbers
    if (numbers_received.length >= 10) {
      numbers_received.shift();
    }
    numbers_received.push(msg.number);
    numbers_string = "";
    for (var i = 0; i < numbers_received.length; i++) {
      numbers_string =
        numbers_string + "<p>" + numbers_received[i].toString() + "</p>";
    }
    $("#log").html(numbers_string);
    console.log(numbers_string);
  });
});
