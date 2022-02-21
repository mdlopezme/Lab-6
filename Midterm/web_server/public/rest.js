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

  user_select();
  door_logs();
  bell_logs();
});

function user_select() {
  console.log('populating select option')
  fetch('/users')
    .then(response=>response.json())
    .then(function(response) {
      let select_box = document.getElementById('door user');
      for(index in response) {
        let theValue = response[index]['value']
        let theText = response[index]['text']
        select_box.options[select_box.options.length] = new Option(theText,theValue);
      }
    })
  console.log('done with user select')
}

function door_control(){
    console.log("Manual Door Override");
    let door_state = document.getElementById("door_cotrol").checked;
    // True is  Unlocked, False is Automatic

    let theUrl = '/override?state=' + door_state;
    fetch(theUrl);
}

function get_URL_params(start_id,end_id) {
  let timeZone=Intl.DateTimeFormat().resolvedOptions().timeZone;
  let startDate=document.getElementById(start_id).value;
  let endDate=document.getElementById(end_id).value;
  if (startDate>endDate) {
    console.log("wrong dates");
    return false;
  }
  return '?start='+startDate+'&end='+endDate+'&timezone='+timeZone;
}

function inject_response(response,tableID) {
  let theTable=document.getElementById(tableID);
  // Clear table
  let rowCount = theTable.rows.length;
  for (let i = 0; i < rowCount; i++) {
      theTable.deleteRow(0);
  }
  // add rows
  if(!response) {
    let theRow = theTable.insertRow();
    theRow.insertCell().innerHTML = "The end date should be after the start date.";
    return;
  }
  if(response['id']=="No records.") {
    console.log("no record response");
    let theRow = theTable.insertRow();
    theRow.insertCell().innerHTML = "No records found.";
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
  let theUser=document.getElementById('door user').value;
  // console.log(theUser)
  let urlParam=get_URL_params('lock-start','lock-end')
  if(!urlParam) {
    inject_response(false,'door log');
    return;
  }
  let theUrl='/door' + urlParam + '&user=' + theUser;
  // console.log(theUrl)
  fetch(theUrl)
    .then(response=>response.json())
    .then(function(response) {
      inject_response(response,'door log');
    })
}

function bell_logs() {
  console.log("Get bell rings.");
  let urlParam=get_URL_params('bell-start','bell-end')
  if(!urlParam) {
    inject_response(false,'bell logs');
    return;
  }
  let theUrl='/bell' + urlParam;
  fetch(theUrl)
    .then(response=>response.json())
    .then(function(response) {
      inject_response(response,'bell logs');
    })
}