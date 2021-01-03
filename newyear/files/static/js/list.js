var input = document.getElementsByClassName("list-input");
var search = document.getElementById("search");
var htmlGoalList = document.getElementById("goalList").children
var goalList = []
var list = []
var typeFor = "goal-element"
var preUUID = document.getElementById("preUUID").innerText
console.log(htmlGoalList)

function setup(){
  //setup modal with inputs from server
  for(var x=0; x<htmlGoalList.length; x++){
    goalList.push(htmlGoalList[x].innerText)
    console.log(htmlGoalList[x].innerText)
  }
  console.log(goalList)
  list = goalList
  editList()

  //add listeners to save on input keyup
  for (var i = 0; i < input.length; i++) {
    addInputListener(input[i])
  }

  //add active listener
  document.getElementById("active").addEventListener('keyup', function(e){
    createItem(document.getElementById("active").value)
    document.getElementById("active").value = ""
  })
}
//create new item on active listener
function createItem(value){
  div = document.createElement("div")
  div.className = "list-element"
  input = document.createElement("input")
  input.type = "checkbox"
  input.id = preUUID+"-checked"
  label = document.createElement("label")
  label.className = "container"
  span = document.createElement("span")
  span.className = "checkmark"
  input2 = document.createElement("input")
  input2.value = value
  input2.id = preUUID+"-input"
  input2.className = "list-input"
  a = document.createElement("A")
  goalType = document.createElement("div")
  goalType.id = preUUID+"-goalType"
  goalType.innerText = "None"
  goalType.className = "goal-type"
  button = document.createElement("BUTTON")
  button.type = "button"
  button.className = "btn btn-primary"
  button.id = preUUID+"-button"
  button.innerText = "Edit Type"

  a.appendChild(goalType)
  label.appendChild(input)
  label.appendChild(span)
  div.appendChild(label)
  div.appendChild(input2)
  div.appendChild(a)
  div.appendChild(button)
  document.getElementById("list").appendChild(div)
  document.getElementById(preUUID+"-button").setAttribute("data-toggle", "modal");
  document.getElementById(preUUID+"-button").setAttribute("data-target", "#addtype");
  document.getElementById(preUUID+"-button").setAttribute("onClick", "changeTypeFor('"+preUUID+"-goalType')");
  document.getElementById(preUUID+"-checked").setAttribute("onClick", "checkBox('"+preUUID+"')");

  addInputListener(document.getElementById(preUUID+"-input"))

  //update info and focus
  document.getElementById(preUUID+"-input").focus()
  document.getElementById(preUUID+"-input").value = value;
  
  //update in database
  makeItem(preUUID)
}

//check for updates needed on input
function addInputListener(input){
  input.addEventListener('keyup', function(e){
    updateItem(this.id.slice(0,-6), false)
  }, false);
}

//check for updates needed on checkbox
function checkBox(uuid){
  updateItem(uuid, false)
}

//type helper 
function changeTypeFor(type){
  console.log("type for called")
  typeFor = type
}

//checks for updates needed on type
function addType(type){
  console.log(typeFor)
  $('#addtype').modal('hide');
  document.getElementById(typeFor).innerText = type
  document.getElementById(typeFor).parentElement.href = "/post/"+type
  updateItem(typeFor.slice(0,-9), false)
}

function updateItem(uuid, isNew){
  listItem = (document.getElementById(uuid+"-input")).value
  goalType = (document.getElementById(uuid+"-goalType")).innerText
  checked = (document.getElementById(uuid+"-checked")).checked
  console.log(goalType)
  itemCall(listItem, goalType, checked, isNew, uuid)
}

function makeItem(uuid){
  updateItem(uuid, true)
}

function itemCall(listItem, goalType, checked, isNew, uuid){
  $.ajax({
    url: "listadd",
    type: "POST",
    data: {"name": listItem, "goalType": goalType, "new": isNew, "uuid": uuid, "checked": checked},
    success: function(result){
      if (result && isNew){
        preUUID = result
      }
    }
  })
}

//update html with searched items
function editList(){
  document.getElementById("typeList").innerHTML = ""
  for(var x=0; x<list.length; x++){
    var div = document.createElement("div")
    div.innerText = list[x];
    div.className = "type-element"
    div.setAttribute("onclick","addType('"+list[x]+"')");
    document.getElementById("typeList").appendChild(div)
  }
}
//search function activation
search.addEventListener("keyup", function(event){
  list = []
  console.log(goalList[0].toLowerCase())
  for(var x=0; x<goalList.length; x++){
    if(goalList[x].toLowerCase().includes(search.value.toLowerCase())){
      list.push(goalList[x])
    }
  }
  console.log(list)
  editList()
})

//setup html
setup()
