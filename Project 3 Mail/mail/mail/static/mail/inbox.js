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


function compose_reply(email) {
  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  // Fill in composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `\n\n---\nOn ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`;
}


function send_email() {
  // Get email to be sent from compose-form
  const formElement = document.forms['compose-form'];
  const formData = new FormData(formElement);

  // Send email
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
      console.log("send_email() success:", result);
  })
  .catch((error) => console.log("send_email() error:", error))
  .finally(() => load_mailbox('inbox'));

  // Block form submission's default behavior 
  return false;
}


function mark_as_read(email, markRead) {
  // If email is currently marked unread, mark as read. Else, mark unread
  // let status = (email.read === false) ? true : false;

  if (email.read != markRead) {
    // Update email's status
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: markRead
      })
    })
    .then(result => {
      console.log("mark_as_read() success:", result);
    })
    .catch((error) => console.log("mark_as_read() error:", error));
  }
  else {console.log("mark_as_read() success: email read status correct")}
}


function mark_as_archived(email, markArchived) {
  // If email is currently marked unarchived, archive it. Else, unarchive it
  // let status = (email.archived === false) ? true : false;

  if (email.archived != markArchived) {
    // Update email's status
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: markArchived
      })
    })
    .then(result => {
      console.log("mark_as_archived() success:", result);
    })
    .catch((error) => console.log("mark_as_archived() error:", error));
  }
  else {console.log("mark_as_archived() success: email archived status correct")}
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  const mailbox_email_view = document.querySelector('#emails-view');
  mailbox_email_view.style.display = 'block';

  // Show the mailbox name
  mailbox_email_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch(`/emails/${mailbox}`)
  .then(result => result.json())
  .then(json => {
    console.log(`mailbox: ${mailbox}`);
    // Show emails    
    json.forEach(email => {
      mailbox_email = show_mailbox_email(email);
      mailbox_email_view.append(mailbox_email);      
      });
    })
  .catch((error) => console.log("load_mailbox() error:", error));
}


function show_mailbox_email(email) {
  console.log(email);

  // Create the email's "mailbox view"
  let mailbox_email = document.createElement('tr');

  // Make the email's view a link to that email
  mailbox_email.addEventListener('click', () => show_email(email));  
  mailbox_email.style.cursor = "pointer";

  // Append some of the email's contents and style to the view
  // If email is unread, bold text for sender, subject, and timestamp 
  let address = document.createElement('td');
  address.textContent = email.sender;
  address.className = (email.read === false) ? "address font-weight-bold" : "address";
  mailbox_email.append(address);

  let subject = document.createElement('td');
  subject.textContent = (email.subject.length <= 20) ? email.subject : email.subject.slice(0, 20).concat("...");
  subject.className = (email.read === false) ? "subject font-weight-bold" : "subject";
  mailbox_email.append(subject);

  let body = document.createElement('td');
  body.className = "body font-weight-light";
  body.textContent = (email.body.length <= 20) ? email.body : email.body.slice(0, 20).concat("...");
  mailbox_email.append(body);

  let timestamp = document.createElement('td');
  const now = new Date();
  const emailtime = new Date(email.timestamp);
  switch (true) {
    // if less than 1 day, show only HH:mm AM
    case (now-emailtime < 24*60*60*1000): 
      timestamp.textContent = email.timestamp.slice(13,);
      break;
    // if less than 1 year, show only Mmm DD
    case (now-emailtime < 365*24*60*60*1000): 
      timestamp.textContent = email.timestamp.slice(0,6);
      break;
    // default: show Mmm DD YYYY, HH:mm AM
    default:
      timestamp.textContent = email.timestamp;
  }
  timestamp.className = (email.read === false) ? "timestamp font-weight-bold" : "timestamp";
  mailbox_email.append(timestamp);
  
  return mailbox_email;
}


function show_email(email) {
  console.log(email);

  // Show only the email view
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  const email_view = document.querySelector('#email-view')
  email_view.style.display = 'block';

  // Don't show prior emails
  email_view.removeChild(email_view.firstChild);

  // Create the email's "message view" & append its contents and style
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

  message.append(document.createElement('hr'));

  let archiveButton = document.createElement('button');
  archiveButton.className = "btn btn-sm btn-outline-primary";
  archiveButton.textContent = (email.archived === false) ? "Move to archive" : "Move to inbox";
  archiveButton.addEventListener('click', () => {
    mark_as_archived(email, true),
    load_mailbox('inbox')
  });
  message.append(archiveButton);

  // If an unread email is viewed, mark it as read
  if (email.read === false) {
    mark_as_read(email, true);
  }

  let unreadButton = document.createElement('button');
  unreadButton.className = "btn btn-sm btn-outline-primary ml-1";
  unreadButton.textContent = "Mark as unread";
  unreadButton.addEventListener('click', () => {
    mark_as_read(email, false), 
    load_mailbox('inbox')
  });
  message.append(unreadButton);

  let replyButton = document.createElement('button');
  replyButton.className = "btn btn-sm btn-outline-primary ml-1";
  replyButton.textContent = "Compose reply"
  replyButton.addEventListener('click', () => compose_reply(email));
  message.append(replyButton);

  email_view.append(message);

  
}
