document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  var buttons = document.querySelectorAll(".edit");
  var dislikes = document.querySelectorAll(".dislike");
  var likes = document.querySelectorAll(".like");



  for (let i = 0, len = buttons.length; i < len; i++) {
    let temp = buttons[i].value;
    buttons[i].addEventListener("click", function(){
      edit_post(temp);
    });

  }

  for (let i = 0, len = dislikes.length; i < len; i++) {
    let temp = dislikes[i].value;
    dislikes[i].addEventListener("click", function(){
      manage_likes(temp,1);
    });

  }

  for (let i = 0, len = likes.length; i < len; i++) {
    let temp = likes[i].value;
    likes[i].addEventListener("click", function(){
      manage_likes(temp,0);
    });

  }



  load_posts();


});


function manage_likes(id,flag){

  event.preventDefault();

  var new_num_likes = document.querySelector(`#likes${id}`);
  //Unarchive
  if(flag == 1){
    fetch(`/manage_likes/${id}`,{
      method: 'PUT',
      body: JSON.stringify({
        like: false
      })
    })
    .then(response => response.json())
    .then(result => {

      var likes = result["likes"];
      var button = document.querySelector(`#change_l${id}`);
      button.style.background = "white";
      new_num_likes.innerHTML = likes;

    })
    .catch(err => console.log(err));

    setTimeout(function(){
      load_posts();
    },250);

  }
  //Archive
  else if(flag == 0){
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
      var button = document.querySelector(`#change_d${id}`);
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
