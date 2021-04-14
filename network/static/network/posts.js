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
