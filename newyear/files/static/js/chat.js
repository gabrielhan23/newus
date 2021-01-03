function addCommentDatabase(comment){
  $.ajax({
    url: "/addComment",
    type: "POST",
    data: {"subpost": comment, "postUUID": getURLPath(), "sid": socketid},
    success: function(data){
      document.getElementById("subposts").innerHTML += "<div class='ubpost'><p>"+data[1]+": "+data[0]+"</p></div>"
    }
  })
}

function addComment(){
  comment = document.getElementById("comment").value
  document.getElementById("comment").value = ""
  addCommentDatabase(comment)  
}

function getURLPath(){
  path = window.location.pathname.split("/")
  return path[2]
}

var socket = io();
var socketid = ''

socket.on('connect', function() {
    socket.emit('begin_chat', {room: getURLPath()});
    socketid = socket.id
});

socket.on('recieveComment', function (data) {
  document.getElementById("subposts").innerHTML += "<div class='ubpost'><p>"+data[1]+": "+data[0]+"</p></div>"
});

var input = document.getElementById("comment")

input.addEventListener("keyup", function(event){
  if(event.keyCode == "13"){
    addComment()
  }
})