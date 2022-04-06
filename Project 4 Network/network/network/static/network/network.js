document.addEventListener("DOMContentLoaded", function () {
  // Autofocus textbox when create-post modal pops up
  $(document).on("shown.bs.modal", function () {
    $("#id_body").focus();
  });

  // Enable tooltips for timestamps
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  // Follow and unfollow creators
  if (document.getElementById("follow-button")) {
    document
      .querySelector("#follow-button")
      .addEventListener("click", function (e) {
        fetch(`/follow/${this.dataset.id}`)
          .then((response) => response.json())
          .then((data) => {
            if (data.user_follows_profile === true) {
              document.querySelector("#is_follower").innerHTML =
                "<strong>you</strong> and ";
              document.querySelector("#follow-button").innerHTML = "Unfollow";
              document.querySelector("#follow-button").className =
                "btn btn-primary btn-sm";
            } else {
              document.querySelector("#is_follower").innerHTML = " ";
              document.querySelector(
                "#follow-button"
              ).innerHTML = `Follow <img src="${this.dataset.img}" width="22">`;
              document.querySelector("#follow-button").className =
                "btn btn-outline-primary btn-sm";
            }
          });
      });
  }
});

//Displays the Unfollow text on the Following button when passing the mouser.
// document
//   .querySelector("#btnfollow")
//   .addEventListener("mouseover", function (event) {
//     if (this.className == "btn btn-primary") {
//       this.innerHTML = "Unfollow";
//     }
//   });

function send_email() {
  // Get email to be sent from compose-form
  const formElement = document.forms["#create-post"];
  const formData = new FormData(formElement);

  // Send email. Then go to sent mail
  fetch("/post", {
    method: "POST",
    post_body: formData,
  })
    .then((response) => response.json())
    .then((result) => console.log("send_email() success:", result))

    .then(() => load_mailbox("sent"))

    .catch((error) => console.log("send_email() error:", error));

  // Block form submission's default behavior
  return false;
}
