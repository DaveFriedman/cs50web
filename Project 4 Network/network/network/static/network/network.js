document.addEventListener("DOMContentLoaded", function () {

  document.querySelector("#create-post-submit")?.addEventListener("submit", submit_post, false);
  document.querySelector(".follow-button ")?.addEventListener("click", follow_profile, false);
  // document.querySelectorAll(".delete-button").forEach(e => e.addEventListener("click", delete_post, false));
  document.querySelectorAll(".edit-button").forEach(e => e.addEventListener("click", edit_post, false));
  document.querySelectorAll(".like-button").forEach(e => e.addEventListener("click", like_post, false));
  document.querySelectorAll(".dislike-button").forEach(e => e.addEventListener("click", dislike_post, false));

  // Autofocus textbox when create-post modal pops up
  $(document).on("shown.bs.modal", function () {
    $("#id_body").focus();
  });

  // Enable bootstrap tooltips for timestamps
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

});

// Bring up edit field for posts
function edit_post() {
  postid = this.dataset.id;

  // footer = document.querySelector(`#post-footer-${postid}`);
  // footer.style.visibility = 'hidden';

  postbody = document.querySelector(`#post-body-${postid}`);
  posttext = document.querySelector(`#post-body-${postid}`).innerText;

  edit_button = document.querySelector(`#edit-button-${postid}`);
  edit_button.setAttribute("data-posttext",`${posttext}` );
  document.querySelectorAll(".edit-button").forEach(e => e.setAttribute("disabled", ""));


  edit_form = create_edit_form(postid, posttext);
  postbody.innerHTML = edit_form;

  edit_post_form = document.querySelector(`#edit-post-form-${postid}`);

  edit_post_form_cancel = document.querySelector(`#edit-post-cancel-${postid}`);
  edit_post_form_cancel.addEventListener("click", () => edit_post_form_cancel_button(postid));

  edit_post_form_submit = document.querySelector(`#edit-post-submit-${postid}`);
  // edited = "April 10th, Right Now";
  // body = "test3\n\n\nnewline";
  edit_post_form_submit.addEventListener("click", () => {
    console.log("edit_post_form_submit()");
    body_update = document.querySelector(`#id_body`).innerText;

    fetch(`/p/${this.dataset.id}/edit`, {
      method: "POST",
      body: body_update // formData.get("body"),
    })
    .then(response => {
      console.log("fetch() .then after response()");
      response.json();
    })
    .then(data =>{
      console.log("fetch() .then after data");
      update_post(data.postid, data.body, data.edited);
    })
  });

  // console.log(postbody);

  // pre_edit_body.append(edit_form);
  // alert(`edit!: ${postid}, ${pre_edit_body}`);

  // update_post(postid, body, edited);

}

function edit_post_form_cancel_button(postid) {
  postbody = document.querySelector(`#edit-button-${postid}`).dataset.posttext;
  document.querySelector(`#post-body-${postid}`).innerText = postbody;

  edit_button = document.querySelector(`#edit-button-${postid}`);
  document.querySelectorAll(".edit-button").forEach(e => e.removeAttribute("disabled"));
}

function create_edit_form(postid, posttext) {

  csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
  let form = `<form id="edit-post-form-${postid}" name="edit-post" action="/p/${postid}/edit" method="POST">`;
  let csrfinput = `<input type="hidden" name="csrfmiddlewaretoken" value="${csrf}"></input>`;
  let div_id_body = `<div id="div_id_body" class="form-group">`;
  let textarea = `<div><textarea name="body" cols="40" rows="6" maxlength="280" class="textarea form-control" required="" id="id_body">${posttext}</textarea></div>`;
  let closediv = `</div>`;
  let footer_div = `<div class="btn-group">`;
  let edit_post_submit = `<input id="edit-post-submit-${postid}" type="submit" value="Update!" class="btn btn-success"></input>`;
  let edit_post_cancel = `<button id="edit-post-cancel-${postid}" type="button" class="btn btn-secondary">Cancel</button>`
  let closeform = `</form>`;

  template = form+csrfinput+div_id_body+textarea+closediv+footer_div+edit_post_submit+edit_post_cancel+closediv+closeform;

  return template;
}

function update_post(postid, body, edited) {

  post_body = document.querySelector(`#post-body-${postid}`);
  post_body.innerText = body;

  if (document.querySelector(`#post-edited-${postid}`)) {
    updated = document.querySelector(`#post-edited-${postid}`)
    updated.setAttribute("data-original-title", `${edited}`);
    updated.textContent = "Updated seconds ago.";
  }
  else {
    let updated = document.createElement('span');
    updated.id = `post-edited-${postid}`;
    updated.className = "text-black-50 time";
    updated.setAttribute("data-toggle", "tooltip");
    updated.setAttribute("data-placement", "top");
    updated.title = "";
    updated.setAttribute("data-original-title", `${edited}`);
    updated.textContent = "Updated seconds ago.";

    document.querySelector(`#post-timestamps-${postid}`).append(updated);

    document.querySelectorAll(".edit-button").forEach(e => e.removeAttribute("disabled"));

    $(function () {
      $('[data-toggle="tooltip"]').tooltip();
    });
  }
  console.log("update_post()");
}

// Update post
function uuuuuupdate_post()
{
  fetch(`/p/${this.dataset.id}/edit`, {
    method: "POST",
    body: "hi" // formData.get("body"),
  })
  .then((response) => response.json())
  .then((data) =>
    update_post(data.postid, data.body, data.edited)
  )
};


 // Follow and unfollow creators
 function follow_profile() {
  fetch(`/follow/${this.dataset.id}`)

  .then((response) => response.json())
  .then((data) => {
    if (data.is_follower === true) {
      document.querySelector("#is_follower_text").innerHTML = "<strong>you</strong> and ";
      document.querySelector("#follow-button-text").innerHTML = "Following";
      document.querySelector("#follow-button").className = "follow-button is_follower btn btn-primary";
      document.querySelector("#follow-img").className = "bi bi-person-plus-fill";
    }
    else {
      document.querySelector("#is_follower_text").innerHTML = " ";
      document.querySelector("#follow-button-text").innerHTML = "Follow";
      document.querySelector("#follow-button").className = "follow-button is_not_follower btn btn-outline-primary";
      document.querySelector("#follow-img").className = "bi bi-person-plus";
    }
  })

  .catch((error) => console.log("follow() error:", error));

};

// Like and unlike posts
function like_post() {
  like_count = parseInt(document.querySelector(`#like-count-${this.dataset.id}`).innerHTML);
  fetch(`/p/${this.dataset.id}/like`)

  .then((response) => response.json())
  .then((data) => {
    if (data.is_liker === true) {
      document.querySelector(`#like-image-${this.dataset.id}`).className = "bi bi-heart-fill";
      document.querySelector(`#like-count-${this.dataset.id}`).innerHTML = like_count+1;
    }
    else {
      document.querySelector(`#like-image-${this.dataset.id}`).className = "bi bi-heart";
      document.querySelector(`#like-count-${this.dataset.id}`).innerHTML = like_count-1;
    }
  })
}


// Dislike and un-dislike posts
function dislike_post() {
  dislike_count = parseInt(document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML);
  fetch(`/p/${this.dataset.id}/dislike`)

  .then((response) => response.json())
  .then((data) => {
    if (data.is_disliker === true) {
      document.querySelector(`#dislike-image-${this.dataset.id}`).className = "bi bi-emoji-angry-fill";
      document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML = dislike_count+1;
    }
    else {
      document.querySelector(`#dislike-image-${this.dataset.id}`).className = "bi bi-emoji-angry";
      document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML = dislike_count-1;
    }
  })
}


//Displays the Unfollow text on the Following button when passing the mouser.
// document
//   .querySelector("#btnfollow")
//   .addEventListener("mouseover", function (event) {
//     if (this.className == "btn btn-primary") {
//       this.innerHTML = "Unfollow";
//     }
//   });

// function send_email() {
//   // Get email to be sent from compose-form
//   const formElement = document.forms["#create-post"];
//   const formData = new FormData(formElement);

//   // Send email. Then go to sent mail
//   fetch("/post", {
//     method: "POST",
//     post_body: formData,
//   })
//     .then((response) => response.json())
//     .then((result) => console.log("send_email() success:", result))

//     .then(() => load_mailbox("sent"))

//     .catch((error) => console.log("send_email() error:", error));

//   // Block form submission's default behavior
//   return false;
// }



// Create new post
function submit_post() {
  const formElement = document.forms["create-post"];
  const formData = new FormData(formElement);

  console.log("hi")
  console.log("formdata:", formData)
  console.log("formdata serialized:", formData.serialize())

  fetch("/post", {
    method: "POST",
    body: JSON.stringify({
      body: formData.get("body"),
    }),
  })
  .then((response) => response.json())
  .then((result => console.log("submit_post() success:", result)))

  .catch((error) => console.log("submit_post() error:", error))
  .finally((result) =>  console.log("hi"),
  console.log("formdata:", formData),
  console.log("formdata serialized:", formData.serialize()))
}