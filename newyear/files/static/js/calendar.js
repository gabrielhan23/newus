var days = document.getElementById("days").children
for(var x=0; x<days.length; x++){
  document.getElementById(days[x].innerText).innerHTML += "<img src='/static/images/gold_star.png' class='calendar-image'>"
  document.getElementById(days[x].innerText).className = "star"
}