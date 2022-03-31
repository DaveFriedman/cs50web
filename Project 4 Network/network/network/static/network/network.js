document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#create-post').onsubmit = send_email;

});


function send_email() {
    // Get email to be sent from compose-form
    const formElement = document.forms['#create-post'];
    const formData = new FormData(formElement);

    // Send email. Then go to sent mail
    fetch('/post', {
      method: 'POST',
      post_body: formData
    })

    .then(response => response.json())
    .then(result => console.log("send_email() success:", result))

    .then(() => load_mailbox('sent'))

    .catch((error) => console.log("send_email() error:", error));

    // Block form submission's default behavior
    return false;
  }