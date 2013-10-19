/*
  Common javascript for trains
*/

/*
  Takes the XML for one trip element and turns it into a simple object.
*/
function objectifyTripXml (xmlEle) {

    var tripObj = {}; 

    tripObj.timeStamp = xmlEle.find('TimeStamp').text();
    tripObj.timeStampDate = new Date(0);
    tripObj.timeStampDate.setUTCSeconds(tripObj.timeStamp);
    tripObj.trip = xmlEle.find('Trip').text();
    tripObj.destination = xmlEle.find('Destination').text();
    tripObj.stop = xmlEle.find('Stop').text();
    tripObj.scheduled = xmlEle.find('Scheduled').text();
    tripObj.scheduledDate = new Date(0);
    tripObj.scheduledDate.setUTCSeconds(tripObj.scheduled);
    tripObj.flag = xmlEle.find('Flag').text();
    tripObj.vehicle = xmlEle.find('Vehicle').text();
    tripObj.latitude = xmlEle.find('Latitude').text();
    tripObj.longitude = xmlEle.find('Longitude').text();
    tripObj.heading = xmlEle.find('Heading').text();
    tripObj.speed = xmlEle.find('Speed').text();
    tripObj.lateness = xmlEle.find('Lateness').text();
    
    tripObj.eta = null;
    tripObj.etaStr = "";
    tripObj.etaMins = "";
    if (tripObj.flag == 'app') {
	// assume approaching means current time
	// plus 2 mins
	tripObj.eta = new Date();
	tripObj.eta.addSeconds(120);
	tripObj.etaStr = tripObj.eta.toString('M/d/yyyy HH:mm');
        tripObj.etaMins = 2;
    } else if (tripObj.flag == 'arr') {
	tripObj.eta = new Date(tripObj.timeStampDate);
	tripObj.etaStr = tripObj.eta.toString('M/d/yyyy HH:mm');
	tripObj.etaMins = "Arriving";
    } else if (tripObj.flag == 'dep') {
	tripObj.eta = "Departed";
	tripObj.etaMins = "Departed";
    } else if (tripObj.lateness) {
	tripObj.eta = new Date(tripObj.scheduledDate);
	tripObj.eta.addSeconds(tripObj.lateness);
	tripObj.etaStr = tripObj.eta.toString('M/d/yyyy HH:mm');
	var etaMs = tripObj.eta.getTime();
        var nowMs = tripObj.timeStampDate.getTime();
        tripObj.etaMins = Math.round((etaMs - nowMs) / (60 * 1000));
    } else {
	tripObj.eta = new Date(tripObj.scheduledDate);
	tripObj.etaStr = tripObj.eta.toString('M/d/yyyy HH:mm');
	var etaMs = tripObj.eta.getTime();
        var nowMs = tripObj.timeStampDate.getTime();
        tripObj.etaMins = Math.round((etaMs - nowMs) / (60 * 1000));
    }
    

    return tripObj;
}
