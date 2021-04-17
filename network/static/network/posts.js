function manage_likes(id, label){

  event.preventDefault();

  var button;

  if(label === "change_l"){

    button = document.querySelector(`#change_l${id}`);


  }

  else if(label === "change_d"){
    button = document.querySelector(`#change_d${id}`);

  }

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


function send_edit_post(id){



  //button of edit post
  var button = document.querySelector('#send');


  // Show compose view and hide other views
  document.querySelector('#all_posts').style.display = 'none';
  document.querySelector('#edit_post').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-body').value = '';

  send.addEventListener('click',() => {
    fetch(`/edit_posts/${id}`,{
      method: 'PUT',
      body: JSON.stringify({
        body: document.querySelector('#compose-body').value

      })
    })
    var paragraph = document.querySelector(`#edit_p${id}`);
    paragraph.innerHTML = document.querySelector('#compose-body').value;
    console.log(paragraph.innerHTML);

    // Show compose view and hide other views
    document.querySelector('#all_posts').style.display = 'block';
    document.querySelector('#edit_post').style.display = 'none';

    // event.preventDefault();




    return false;
  });


}
