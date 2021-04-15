
var dislikes;
var likes;
document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  var buttons = document.querySelectorAll(".edit");

  for (let i = 0, len = buttons.length; i < len; i++) {
    let temp = buttons[i].value;
    buttons[i].addEventListener("click", function(){
      edit_post(temp);
    });

  }


  load_posts();


});


function manage_likes(id, label){

  event.preventDefault();

  // var flag;
  var button;

  if(label === "change_l"){

    // flag = document.querySelector(`#dislike${id}`);
    button = document.querySelector(`#change_l${id}`);


  }

  else if(label === "change_d"){
    // flag = document.querySelector(`#like${id}`);
    button = document.querySelector(`#change_d${id}`);

  }

  console.log(window.getComputedStyle(button, null).getPropertyValue("background-color"));




  var new_num_likes = document.querySelector(`#likes${id}`);
  //Unarchive
  if(window.getComputedStyle(button, null).getPropertyValue("background-color") === "rgb(255, 0, 0)"){
    fetch(`/manage_likes/${id}`,{
      method: 'PUT',
      body: JSON.stringify({
        like: false
      })
    })
    .then(response => response.json())
    .then(result => {

      var likes = result["likes"];
      new_num_likes.innerHTML = likes;
      console.log(button);
      button.style.background = "white";



    })
    .catch(err => console.log(err));

    setTimeout(function(){
      load_posts();
    },250);

  }
  //Archive
  else if(window.getComputedStyle(button, null).getPropertyValue("background-color") === "rgb(255, 255, 255)"){
    fetch(`/manage_likes/${id}`,{
      method: 'PUT',
      body: JSON.stringify({
        like: true
      })
    })
    .then(response => response.json())
    .then(result => {

      var likes = result["likes"];
      new_num_likes.innerHTML = likes;
      console.log(button);
      button.style.background = "red";

    })
    .catch(err => console.log(err));

    setTimeout(function(){
      load_posts();
    },250);

  }





}


function edit_post(id) {

  event.preventDefault();

  console.log(id);



  // Show compose view and hide other views
  document.querySelector('#all_posts').style.display = 'none';
  document.querySelector('#edit_post').style.display = 'block';



  // Clear out composition fields
  document.querySelector('#compose-body').value = '';

  // Form that sends the email info
  document.querySelector('#compose-form').addEventListener('submit', () => send_edit_post(id));

}


function send_edit_post(id){



  fetch(`/edit_posts/${id}`,{
    method: 'PUT',
    body: JSON.stringify({
      body: document.querySelector('#compose-body').value
    })
  })
  setTimeout(function(){
    load_posts();
  },250);


}





function load_posts(){

  // Show compose view and hide other views
  document.querySelector('#all_posts').style.display = 'block';
  document.querySelector('#edit_post').style.display = 'none';



}
