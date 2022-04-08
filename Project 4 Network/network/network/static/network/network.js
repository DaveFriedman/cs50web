document.addEventListener("DOMContentLoaded", function () {


  document.querySelector("#create-post-submit")?.addEventListener("submit", submit_post, false);
  document.querySelector(".follow-button ")?.addEventListener("click", follow_profile, false);
  document.querySelectorAll(".like-button").forEach(e => e.addEventListener("click", like_post, false));

  // Autofocus textbox when create-post modal pops up
  $(document).on("shown.bs.modal", function () {
    $("#id_body").focus();
  });

  // Enable tooltips for timestamps
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
});

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
