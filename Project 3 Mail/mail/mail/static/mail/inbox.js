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
  document.querySelector('#mailbox-view').style.display = 'none';

  // Set header
  document.querySelector('#compose-header').innerText = 'New Email';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function compose_reply(email) {
  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#mailbox-view').style.display = 'none';

  // Set header
  document.querySelector('#compose-header').innerText = `Reply to: ${email.sender}`;

  // Fill in composition fields
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  document.querySelector('#compose-subject').value = (email.subject.slice(0, 4) === "Re: ") ? `${email.subject}` : `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `\n\n---\nOn ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`;
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  const mailbox_view = document.querySelector('#mailbox-view');
  mailbox_view.style.display = 'block';

  // Show the mailbox name
  mailbox_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch emails
  fetch(`/emails/${mailbox}`)
  .then(result => result.json())
  .then(json => {
    console.log(`mailbox: ${mailbox}`);
    // Show emails
    json.forEach(email => {
      email_summary = show_email_summary(email, mailbox);
      mailbox_view.append(email_summary);
    });
  })
  .catch((error) => console.log("load_mailbox() error:", error));
}


function show_email_summary(email, mailbox) {
  console.log(email);

  // Create the email's summary
  let email_summary = document.createElement('tr');

  // Make the email's summary a link to that email
  email_summary.addEventListener('click', () => show_email(email, mailbox));
  email_summary.style.cursor = "pointer";

  // Append some of the email's contents and style to the summary
  // If email is unread, bold text for sender, subject, and timestamp
  let address = document.createElement('td');
  // If showing sent mail, don't show the sender (aka the user). Instead, show up to 2 recipients
  address.textContent = (mailbox != 'sent') ? email.sender : ((email.recipients.length > 1) ? `To: ${email.recipients[0]}, ${email.recipients[1]}...` : `To: ${email.recipients}`);
  address.className = (email.read === false) ? "address font-weight-bold" : "address";
  email_summary.append(address);

  let subject = document.createElement('td');
  subject.textContent = (email.subject.length <= 20) ? email.subject : email.subject.slice(0, 20).concat("...");
  subject.className = (email.read === false) ? "subject font-weight-bold" : "subject";
  email_summary.append(subject);

  let body = document.createElement('td');
  body.className = "body font-weight-light";
  body.textContent = (email.body.length <= 20) ? email.body : email.body.slice(0, 20).concat("...");
  email_summary.append(body);

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
  email_summary.append(timestamp);

  return email_summary;
}


function show_email(email, mailbox) {
  console.log(email);

  // Show only the email view
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mailbox-view').style.display = 'none';
  const email_view = document.querySelector('#email-view')
  email_view.style.display = 'block';

  // Don't show prior emails
  email_view.removeChild(email_view.firstChild);

  // If an unread email is viewed, mark it as read
  if (email.read === false) mark_as_read(email);

  // Create the email
  let message = document.createElement('div');
  message.className = "email";

  // Create and append the email's contents and style
  let sender = document.createElement('p');
  sender.innerHTML = `<strong>From:</strong> ${email.sender}`;
  message.append(sender);

  let recipients = document.createElement('p');
  recipients.innerHTML = `<strong>To:</strong> ${email.recipients.join(", ")}`;
  message.append(recipients);

  let subject = document.createElement('p');
  subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
  message.append(subject);

  let timestamp = document.createElement('p');
  timestamp.innerHTML = `<strong>Sent:</strong> ${email.timestamp}`;
  message.append(timestamp);

  message.append(document.createElement('hr'));

  let body = document.createElement('p');
  body.innerText = email.body;
  message.append(body);

  message.append(document.createElement('hr'));

  // Create and append reply button, sending email to fill in compose_reply data
  let replyButton = document.createElement('button');
  replyButton.className = "btn btn-sm btn-outline-primary";
  replyButton.textContent = "Compose reply"
  replyButton.addEventListener('click', () => compose_reply(email));
  message.append(replyButton);

  // Create and append the archive/inbox button
  let archiveButton = document.createElement('button');
  archiveButton.className = "btn btn-sm btn-outline-primary  ml-1";
  archiveButton.textContent = (email.archived === false) ? "Move to archive" : "Move to inbox";
  archiveButton.addEventListener('click', () => switch_isArchived(email));
  // Don't allow archiving of sent emails
  if (mailbox != 'sent') message.append(archiveButton);

  email_view.append(message);
}


function send_email() {
  // Get email to be sent from compose-form
  const formElement = document.forms['compose-form'];
  const formData = new FormData(formElement);

  // Send email. Then go to sent mail
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: formData.get('compose-recipients'),
        subject: formData.get('compose-subject'),
        body: formData.get('compose-body')
    })
  })

  .then(response => response.json())
  .then(result => console.log("send_email() success:", result))

  .then(() => load_mailbox('sent'))

  .catch((error) => console.log("send_email() error:", error));

  // Block form submission's default behavior
  return false;
}


function mark_as_read(email) {
  // Mark an email as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  .then(response => response.json())
  .then(result => console.log("mark_as_read() success:", result))
  .catch((error) => console.log("mark_as_read() error:", error));
}


function switch_isArchived(email) {
  // If email is unarchived, archive it. Else, unarchive it. Then, go to inbox
  let status = (email.archived === false) ? true : false;

  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: status
    })
  })

  .then(response => response.json())
  .then(result => console.log("switch_isArchived() success:", result))

  .then(() => load_mailbox('inbox'))

  .catch((error) => console.log("switch_isArchived() error:", error));
}