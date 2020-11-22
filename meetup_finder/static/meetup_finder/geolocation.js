/***************************************************************************************
*  REFERENCES
*  Title: Function to calculate distance between two coordinates
*  Author: Airikr
*  Date: 2013-09-18
*  URL: https://stackoverflow.com/questions/18883601/function-to-calculate-distance-between-two-coordinates
*  Software License: CC BY-SA 3.0
*
*  Title: Easiest way to sort DOM nodes?
*  Author: nickf
*  Date: 2008-11-12
*  URL: https://stackoverflow.com/questions/282670/easiest-way-to-sort-dom-nodes/282711#282711
*  Software License: CC BY-SA 2.5
*
***************************************************************************************/

function filterEvents() {
	$(".event").css("display", "block");
	if ($("#filter").val() !== "") {
		$("#clear-filter").html("Clear filters");
		$("#clear-filter").prop("disabled", false);
	} else {
		clearFilters();
	}

	var query = $("#filter").val().toLowerCase().split(",");
	if (query.length > 1 || query[0] !== "") {
		var match = function(index, element) {
			for (var i = 0; i < query.length; i++) {
				if ($(element).text().toLowerCase().indexOf(query[i]) > -1 && query[i].length > 0) {
					return false; // matches query
				}
			}
			return true; // does not match query
		}
		$(".event").filter(match).css("display", "none"); // hides elements that do not match query
	}
}

function clearFilters() {
	$("#filter").val("");
	$(".event").css("display", "block");
	$("#clear-filter").html("Filter cleared");
	$("#clear-filter").prop("disabled", true);
}

function sortByDistance() {
	navigator.geolocation.getCurrentPosition(sortByDistanceCallback);
}

function getEventDistance() {
	navigator.geolocation.getCurrentPosition(getEventDistanceCallback);
}

function getEventDistanceCallback(pos) {
	var myLat = pos.coords.latitude; // parse user coords
	var myLong = pos.coords.longitude;

	var eventLat = coordinates[0]; // parse event coords
	var eventLong = coordinates[1];
	var distance = getDistanceBetween(myLat, myLong, eventLat, eventLong);
	document.getElementById("distance").innerHTML = " (" + distance.toFixed(1) + " mi away)";
}

function sortByDistanceCallback(pos) {
	var myLat = pos.coords.latitude; // parse user coords
	var myLong = pos.coords.longitude;
	var distances = {};
	for (var event in coordinates) {
		if (coordinates.hasOwnProperty(event)) {
			var eventLat = coordinates[event].split(',')[0]; // parse event coords
			var eventLong = coordinates[event].split(',')[1];
			var distance = getDistanceBetween(myLat, myLong, eventLat, eventLong);
			distances[event] = distance;
			$("#distance-" + event).html("(" + distance.toFixed(1) + " mi away)");
		}
	}
	
	// https://stackoverflow.com/questions/282670/easiest-way-to-sort-dom-nodes
	// modified to fit the page structure
	var list = $("#event-list")[0];
	
	var items = list.childNodes;
	var itemsArr = [];
	for (var i in items) {
		if (items[i].nodeType == 1) { // get rid of the whitespace text nodes
			itemsArr.push(items[i]);
		}
	}

	itemsArr.sort(function(a, b) {
		a = distances[a.getAttribute("data-pk")];
		b = distances[b.getAttribute("data-pk")];
		return a == b ? 0 : (a > b ? 1 : -1);
	});

	for (i = 0; i < itemsArr.length; ++i) {
		list.appendChild(itemsArr[i]);
	}
	
	$("#sort-button").html("Sorted by distance");
	$("#sort-button").prop("disabled", true);
}

// https://stackoverflow.com/questions/18883601/function-to-calculate-distance-between-two-coordinates
// modified to return distance in miles rather than km
function getDistanceBetween(lat1, lon1, lat2, lon2) {
	var R = 3958.761; // Radius of the earth in miles
	var dLat = deg2rad(lat2-lat1);  // deg2rad below
	var dLon = deg2rad(lon2-lon1); 
	var a = 
		Math.sin(dLat/2) * Math.sin(dLat/2) +
		Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
		Math.sin(dLon/2) * Math.sin(dLon/2); 
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
	var d = R * c; // Distance in miles
	return d;
}

function deg2rad(deg) {
	return deg * (Math.PI/180)
}