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
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';


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
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  const mailbox_email_div = document.querySelector('#emails-view');
  mailbox_email_div.style.display = 'block';


  // Show the mailbox name
  mailbox_email_div.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch('/emails/inbox')
  .then(response => response.json())
  .then(json => {

    // Show emails    
    json.forEach(email => {
        const mailbox_email = show_mailbox_email(email);
        mailbox_email_div.append(mailbox_email);
      });
  });
}


function show_mailbox_email(email) {
  console.log(email);

  // mailbox_email.className = "row";
  let mailbox_email = document.createElement('tr');
  mailbox_email.addEventListener('click', () => show_email(email));  
  mailbox_email.style.cursor = "pointer";

  let address = document.createElement('td');
  address.textContent = email.sender;
  mailbox_email.append(address);

  let subject = document.createElement('td');
  subject.textContent = email.subject;
  mailbox_email.append(subject);

  // body.textContent = (email.body.length <= 10) ? email.body : email.body.slice(0, 10).concat("...");
  let body = document.createElement('td');
  body.className = "body font-weight-light";
  body.textContent = email.body;
  mailbox_email.append(body);

  let timestamp = document.createElement('td');
  timestamp.textContent = email.timestamp;
  mailbox_email.append(timestamp);

  
  return mailbox_email;
}


function show_email(email) {
  console.log(email);

  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  const email_div = document.querySelector('#email-view')
  email_div.style.display = 'block';
  email_div.removeChild(email_div.firstChild);

  let message = document.createElement('div');
  message.className = "email";

  let sender = document.createElement('p');
  sender.innerHTML = `<strong>From:</strong> ${email.sender}`;
  message.append(sender);

  let recipients = document.createElement('p');
  recipients.innerHTML = `<strong>To:</strong> ${email.recipients}`;
  message.append(recipients);

  let subject = document.createElement('p');
  subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
  message.append(subject);

  let timestamp = document.createElement('p');
  timestamp.innerHTML = `<strong>Sent:</strong> ${email.timestamp}`;
  message.append(timestamp);

  message.append(document.createElement('hr'));

  let body = document.createElement('p');
  body.textContent = email.body;
  message.append(body);

  email_div.append(message);
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