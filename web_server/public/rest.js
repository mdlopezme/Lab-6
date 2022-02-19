function door_control(){
    console.log("com")
    // door_state = document.getElementById("height").value.split("-");
    // age_range = document.getElementById("age").value.split("-");

    // theUrl = '/table/' + height_range[0] + '_' + height_range[1] + '_' + age_range[0] + '_' + age_range[1]

    // fetch(theUrl)
    // .then(function(response) {
    //     return response.text()
    // })
    // .then(function(html) {
    //     let parser = new DOMParser();
    //     let doc = parser.parseFromString(html, "text/html");

    //     let newtable = doc.getElementById('container').innerHTML;
    //     document.getElementById("container").innerHTML = newtable;
    // })
    // .catch(function(err) {  
    //     console.log('Failed to fetch page: ', err);  
    // });
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
      console.log(response[key])
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
}