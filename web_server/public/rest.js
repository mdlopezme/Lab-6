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

function door_logs() {

  console.log("Get door attempts.");
  let startDate=document.getElementById('lock-start').value;
  let endDate=document.getElementById('lock-end').value;
  let theUrl='/door?start='+startDate+'&end='+endDate;

  let theTable=document.getElementById('door log');
  console.log(theTable);

  // let newTable=document.createElement('tbody');
  // theTable.parentNode.replaceChild(newTable, theTable);

  console.log(theUrl);
  fetch(theUrl)
    .then(response=>response.json())
    .then(function(response) {
      let rowCount = theTable.rows.length;
      for (let i = 0; i < rowCount; i++) {
          theTable.deleteRow(0);
      }
      
      console.log(response['id']);
      if(response['id']=="No records.") {
        console.log("no record response")
        // document.getElementById('door log')
        //   .innerHTML="";
        let theRow = theTable.insertRow();
        theRow.insertCell().innerHTML = "No records found."
      }
      else {
        for (const key in response) {
          console.log(response[key])
          let theRow = theTable.insertRow();
          theRow.insertCell().innerHTML = response[key]['id'];
          theRow.insertCell().innerHTML = response[key]['name'];
          theRow.insertCell().innerHTML = response[key]['timestamp'];
          theRow.insertCell().innerHTML = response[key]['success'];
        }
      }
    })
  
}

function bell_logs() {
    console.log("Get bell rings.");
}