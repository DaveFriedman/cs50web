document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').onsubmit = send_email;
  
  // By default, load the inbox
  load_mailbox('inbox');
});
  
function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function send_email() {
  const formElement = document.forms['compose-form'];
  const formData = new FormData(formElement);

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: formData.get('compose-recipients'),
        subject: formData.get('compose-subject'),
        body: formData.get('compose-body')
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
  })
  .catch((error) => console.log(error));

  return false;
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(json => {

    // Print emails    
    const mailbox_email_div = document.querySelector('#emails-view');
    json.forEach(email => {

      if (email.archived === false) {
        const mailbox_email = show_mailbox_email(email);
        if (email.unread === true) {
          // TODO
        }
        mailbox_email_div.append(mailbox_email);
      }
    });
  });
}

function show_mailbox_email(email) {
  console.log(email);

  let mailbox_email = document.createElement('div');
  mailbox_email.className = "row";

  let address = document.createElement('div');
  address.className = "address col-3";
  address.textContent = `${email.sender}`;
  mailbox_email.append(address);

  let subject = document.createElement('div');
  subject.className = "subject col-6";
  subject.textContent = email.subject.concat("  ");
  mailbox_email.append(subject);

  let body = document.createElement('span');
  body.className = "body font-weight-light";
  body.textContent = (email.body.length <= 10) ? email.body : email.body.slice(0, 10).concat("...");
  subject.append(body);

  let timestamp = document.createElement('div');
  timestamp.className = "timestamp col-3";
  timestamp = email.timestamp;
  mailbox_email.append(timestamp);

  return mailbox_email;
}







//         let emailDiv = document.createElement('li');
// archived
// body
// id
// read
// recipients
// sender
// subject
// timestamp