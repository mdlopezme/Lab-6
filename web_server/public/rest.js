document.addEventListener("DOMContentLoaded", function() {
  var dateObj = new Date();

  var day = ("0" + dateObj.getDate()).slice(-2);
  var month = ("0" + (dateObj.getMonth() + 1)).slice(-2);
  var today = dateObj.getFullYear()+"-"+(month)+"-"+(day) ;

  document.getElementById('lock-start').value=today;
  document.getElementById('lock-end').value=today;
  document.getElementById('bell-start').value=today;
  document.getElementById('bell-end').value=today;

  document.getElementById('lock-start').max=today;
  document.getElementById('lock-end').max=today;
  document.getElementById('bell-start').max=today;
  document.getElementById('bell-end').max=today;

  door_logs();
  bell_logs();
});

function door_control(){
    console.log("Manual Door Override")
    door_state = document.getElementById("door_cotrol").checked
    // True is  Unlocked, False is Automatic

    theUrl = '/override?state=' + door_state
    fetch(theUrl)
}

function get_URL_params(start_id,end_id) {
  let timeZone=Intl.DateTimeFormat().resolvedOptions().timeZone
  let startDate=document.getElementById(start_id).value;
  let endDate=document.getElementById(end_id).value;
  return '?start='+startDate+'&end='+endDate+'&timezone='+timeZone;
}

function inject_response(response,tableID) {
  let theTable=document.getElementById(tableID);
  // Clear table
  let rowCount = theTable.rows.length;
  for (let i = 0; i < rowCount; i++) {
      theTable.deleteRow(0);
  }

  if(response['id']=="No records.") {
    console.log("no record response")
    let theRow = theTable.insertRow();
    theRow.insertCell().innerHTML = "No records found."
  }
  else {
    for (const key in response) {
      // console.log(response[key])
      let theRow = theTable.insertRow();
      for (const innerKey in response[key]) {
        theRow.insertCell().innerHTML=response[key][innerKey];
      }
    }
  }
}

function door_logs() {
  console.log("Get door attempts.");
  let theUrl='/door' + get_URL_params('lock-start','lock-end')
  fetch(theUrl)
    .then(response=>response.json())
    .then(function(response) {
      inject_response(response,'door log');
    }
    )
}

function bell_logs() {
    console.log("Get bell rings.");
    let theUrl='/bell' + get_URL_params('bell-start','bell-end')
    fetch(theUrl)
    .then(response=>response.json())
    .then(function(response) {
      inject_response(response,'bell logs');
    }
    )
}