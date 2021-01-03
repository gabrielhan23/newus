postsList = document.getElementsByClassName("post-title")
posts = []
searchPosts = []
function setup(){
  for(var x=0; x<postsList.length; x++){
    console.log(postsList[x])
    posts.push([postsList[x].innerText, postsList[x].id, postsList[x].getAttribute("alt")])
  }
  searchPosts = posts
  console.log(posts)
  document.getElementById("page-title").innerText = getURLPath()+" - Forum"
}

function addPostDatabase(title, body){
  $.ajax({
    url: "/addpost",
    type: "POST",
    data: {"title": title, "body": body, "goalType": getURLPath()},
    success: function(result){
      document.getElementById("posts").innerHTML += "<tr class='post'><td class='td-user'><img src='/static/images/usericon.png' class='right-image user-image'></td><td class='td-title'><a href='/chat/"+result+"'><h1 class='post-title'>"+title+"</h1></a></td><td><p>0 Answers</p></td><td><img src='/static/images/thumbs up.png')}}' class='right-image thumbs-image'></td></tr>"
    }
  })
}

function addPost(){
  title = document.getElementById("title").value
  body = document.getElementById("body").value
  console.log(title)
  console.log(getURLPath())
  addPostDatabase(title, body)  
}

function getURLPath(){
  path = window.location.pathname.split("/")
  return path[2].replace("%20", " ")
}


//update html with searched items
function editList(){
  document.getElementById("posts").innerHTML = ""
  for(var x=0; x<searchPosts.length; x++){
    document.getElementById("posts").innerHTML += "<tr class='post'><td class='td-user'><img src='/static/images/usericon.png' class='right-image user-image'></td><td class='td-title'><a href='/chat/"+searchPosts[x][1]+"'><h1 class='post-title'>"+searchPosts[x][0]+"</h1></a></td><td><p>"+searchPosts[x][2]+" Answers</p></td><td><img src='/static/images/thumbs up.png')}}' class='right-image thumbs-image'></td></tr>"
  }
}
//search function activation
search.addEventListener("keyup", function(event){
  searchPosts = []
  for(var x=0; x<posts.length; x++){
    if(posts[x][0].toLowerCase().includes(search.value.toLowerCase())){
      searchPosts.push(posts[x])
    }
  }
  console.log(searchPosts)
  editList()
})

setup()