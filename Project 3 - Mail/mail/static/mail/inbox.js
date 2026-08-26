document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', sendEmail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sendEmail(event){
  event.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox('sent');
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/'+ mailbox, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(emails =>{
    document.querySelector('#emails-view').innerHTML = '';
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    emails.forEach(email => {
      const div = document.createElement('div');
      div.innerHTML = `Sender: ${email.sender}" " Subject: ${email.subject}" " Timestamp: ${email.timestamp}`;
      if(email.read === true){
        div.style.background = "gray";
      }else{
        div.style.background = "white";
      }
      const emailsView = document.querySelector('#emails-view');
      div.addEventListener('click', () => viewEmail(email.id, mailbox))
      emailsView.appendChild(div);
    })
  })
}

function viewEmail(email_id, mailbox){
  fetch('/emails/' + email_id, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(email =>{
    document.querySelector('#email-view').innerHTML = "";
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector("#email-view").style.display = 'block';
    const div = document.createElement('div');
    div.innerHTML = `Sender: ${email.sender}<br>
                   Recipients: ${email.recipients}<br>
                   Subject: ${email.subject}<br>
                   Timestamp: ${email.timestamp}<br>
                   Body: ${email.body}<br>`
    const emailView = document.querySelector('#email-view');
    const button = document.createElement("button");
    if(mailbox !== 'sent'){
      if(email.archived === true){
        button.innerHTML = 'Unarchive';
      }else{
        button.innerHTML = 'Archive';
      }
      emailView.appendChild(button);
      button.addEventListener('click', () => {
        fetch('/emails/' + email_id, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        })
        .then(() => {
          load_mailbox('inbox');
        });
      });
    }
    const replyButton = document.createElement('button');
    replyButton.innerHTML = 'Reply';
    replyButton.addEventListener('click', () => {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      if (email.subject.startsWith('Re:')) {
        document.querySelector('#compose-subject').value = email.subject;
      }
      else {
        document.querySelector('#compose-subject').value = "Re: " + email.subject;
      }
      document.querySelector('#compose-body').value = "On " + email.timestamp + " " + email.sender + " wrote:\n\n" + email.body;
    });
    emailView.appendChild(replyButton);
    emailView.appendChild(div);
    fetch('/emails/'+ email_id, {
      method: 'PUT',
      body: JSON.stringify({
        read: true,
      })
    })
  })
}