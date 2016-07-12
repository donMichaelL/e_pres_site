$(document).ready(function() {

chart = null;
topicNode = null;

client = new Paho.MQTT.Client(host, Number(port), "web_" + parseInt(Math.random() * 100));
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
client.connect({onSuccess:onConnect});

var row = -1;


function onConnect() {
  console.log("onConnect");
  $("#start").removeClass('hidden');
  client.subscribe(topic);
}

function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage + " "+ responseObject.errorCode);
  }
}


function onMessageArrived(message) {
  var jsonMessage = JSON.parse(message.payloadString);
  if(message.destinationName == 'output/error'){
    var probleMessage = translateErrorCode(jsonMessage.errorCode);
    $('#eventsFeed').prepend('<li class="list-group-item list-group-item-danger">'+ probleMessage +'</li>');
  }
  else {
    var number = jsonMessage.flux;
    var tpc = jsonMessage.antenna;

    var node = '#node'+ tpc;
    var progress = "#progress" + tpc;
    var marker = eval('marker' + tpc)
    var nodeNumber = marker.options.icon.options.number;
    var maxFluxCurrentNode = marker.options.icon.options.flux;
    var result = (parseInt(number)/ maxFluxCurrentNode) * 100;


    $(node).html(number);
    $(progress).width(result + "%");
    marker._icon.childNodes[1].innerHTML =  nodeNumber + ":" + number.toString();
    if(dangerousValue(parseInt(number), maxFluxCurrentNode)){
    	$(node).parent().addClass('alert-box');
  	  marker._icon.childNodes[0].src = "/static/img/danger.png";
    	$(progress).addClass('progress-bar-danger');
      }else {
    	   $(node).parent().removeClass('alert-box');
    	    if(tpc == row) {
            marker._icon.childNodes[0].src = "/static/img/target.png";
          }
    	     else {
             marker._icon.childNodes[0].src = "/static/img/raspi.png";
           }
    	$(progress).removeClass('progress-bar-danger');
    }

    nodeforMap = '#node' + nodeNumber;


    if (topicNode == nodeforMap) {
    	if(dangerousValue(parseInt(number), maxFluxCurrentNode)) {
        chart.options.data[0].color = "#F57676";
        chart.options.data[0].markerColor = "#F57676";
    	}else {
        chart.options.data[0].color = "black";
        // chart.options.data[0].markerColor = "red";
    	}
    	updateGraph(parseInt(number));
    }
  }
}


function dangerousValue(value, limit){
	if (value > limit && limit > 1) {
		return true;
	}
	return false;
}

function updateGraph(new_value){
	var length = chart.options.data[0].dataPoints.length;
	// chart.options.title.text = "New DataPoint Added at the end";
	chart.options.data[0].dataPoints.push({ y: new_value});
	chart.render();
};

function translateErrorCode(errorCode){
  switch(parseInt(errorCode)) {
    case 1:
        return 'Not Correct Path';
        break;
    case 2:
        return 'Not Path After Path';
        break;
  };
};

}) ;
