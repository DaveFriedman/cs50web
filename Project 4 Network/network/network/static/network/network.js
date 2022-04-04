document.addEventListener("DOMContentLoaded", function () {
  // Autofocus textbox when create-post modal pops up
  $(document).on("shown.bs.modal", function () {
    $("#id_body").focus();
  });

  // Enable tooltips for timestamps
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
});

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
