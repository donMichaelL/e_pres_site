$(document).ready(function() {

chart = null;
topicNode = null;

client = new Paho.MQTT.Client(host, Number(port), "web_" + parseInt(Math.random() * 100));
// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});

var row = -1;

// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");

  client.subscribe(topic);
  // message = new Paho.MQTT.Message("The Test message  15 send by HTTP");
  // message.destinationName = "22";
  // client.send(message);
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage + " "+ responseObject.errorCode);
  }

	  // setTimeout(function () {
   //      location.reload();
   //  }, 1);

	// client.connect();
	// client.subscribe(topic);

	// var another = new Paho.MQTT.Client(host, Number(port), "clientId");
	// console.log('hello');
	// another.onConnectionLost = onConnectionLost;
	// another.onMessageArrived = onMessageArrived;
	// another.connect({onSuccess:onConnect});

}


// called when a message arrives
function onMessageArrived(message) {
  console.log(message.payloadString);
  var jsonMessage = JSON.parse(message.payloadString);
  console.log(jsonMessage);

  var number = jsonMessage.flux;
  var tpc = jsonMessage.antenna;

  var node = '#node'+ tpc;
  //var badge = '#badge' + tpc;
  var progress = "#progress" + tpc;
  var max = 10;
  var result = (parseInt(number)/ max) * 100;


  $(node).html(number);
  $(progress).width(result + "%");
  //marker[tpc-1]._icon.childNodes[1].innerHTML = tpc.toString() + ":" + number.toString();
  if(dangerousValue(parseInt(number), parseInt(tpc))){
  	$(node).addClass('alert');
  	$(badge).addClass('alert');
	marker[tpc-1]._icon.childNodes[0].src = "img/danger.png";
  	$(progress).addClass('progress-bar-danger');
  }else {
	$(node).removeClass('alert');
	//$(badge).removeClass('alert');
	// if(tpc == row) {marker[tpc-1]._icon.childNodes[0].src = "img/target.png";}
	// else {marker[tpc-1]._icon.childNodes[0].src = "img/raspi.png";}
	// $(progress).removeClass('progress-bar-danger');
  }


  if (topicNode == node) {
  	// if(dangerousValue(parseInt(number), parseInt(tpc))) {
		// chart.options.data[0].color = "#F57676";
		// chart.options.data[0].markerColor = "#F57676";
  	// }else {
		// chart.options.data[0].color = "black";
		// chart.options.data[0].markerColor = "red";
  	// }
  	updateGraph(parseInt(number));
  }
}


function dangerousValue(value, node){
	var limit = node * 10 ;
	if (value > limit) {
		return true;
	}
	return false;
}


function updateGraph(new_value){
  console.log('h');
	var length = chart.options.data[0].dataPoints.length;
	// chart.options.title.text = "New DataPoint Added at the end";
	chart.options.data[0].dataPoints.push({ y: new_value});
	chart.render();
};


}) ;
