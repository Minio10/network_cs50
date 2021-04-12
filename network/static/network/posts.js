document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#edit').addEventListener('click', edit_post);

  load_posts();


});


function edit_post() {

  event.preventDefault();


  // Show compose view and hide other views
  document.querySelector('#all_posts').style.display = 'none';
  document.querySelector('#edit_post').style.display = 'block';



  // Clear out composition fields
  document.querySelector('#compose-body').value = '';

  // Form that sends the email info
  document.querySelector('#compose-form').addEventListener('submit', send_edit_post);

}


function send_edit_post(){


  var id = document.querySelector('#calmo').value; //value of the text input


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
