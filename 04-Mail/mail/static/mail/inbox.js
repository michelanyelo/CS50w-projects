let current_mailbox = 'inbox'; // global variable to keep track of the current mailbox

document.addEventListener('DOMContentLoaded', function () {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => { current_mailbox = 'inbox'; load_mailbox('inbox'); });
  document.querySelector('#sent').addEventListener('click', () => { current_mailbox = 'sent'; load_mailbox('sent'); });
  document.querySelector('#archived').addEventListener('click', () => { current_mailbox = 'archive'; load_mailbox('archive'); });
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-details-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function formatDate(timestamp) {
  const emailDate = new Date(timestamp);
  const currentDate = new Date();

  if (emailDate.toDateString() === currentDate.toDateString()) {
    return emailDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else {
    return emailDate.toLocaleDateString([], { day: '2-digit', month: 'short' });
  }
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show the emails for mailbox and user
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(singleEmail => {
        displayEmail(singleEmail);
      });
    });
}

function send_email(event) {
  event.preventDefault();

  // Storing fields
  const recipient = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Sending data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipient,
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      load_mailbox('sent');
    });
}

function view_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(singleEmail => {
      displayEmailDetails(singleEmail);
      markEmailAsRead(singleEmail.id);
      const replyButton = createReplyButton(singleEmail);
      let archiveButton = createArchiveButton(singleEmail);
      if (archiveButton !== null) {
        document.querySelector('#email-details-view').append(replyButton, archiveButton);
      } else {
        document.querySelector('#email-details-view').append(replyButton);
      }
    });
}

function displayEmail(singleEmail) {
  const email = document.createElement('div');
  email.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center", "py-3", "border-bottom");
  email.style.cursor = "pointer";

  email.innerHTML = `
    <table style="width:100%">
      <tr>
        <td style="width:30%">${singleEmail.sender}</td>
        <td style="width:20%"> ${singleEmail.subject}</td>
        <td style="width:40%"> ${singleEmail.body}</td>
        <td style="width:10%"> ${formatDate(singleEmail.timestamp)}</td>
      </tr>
    </table>
  `;

  email.classList.add(singleEmail.read ? 'read' : 'unread');

  email.addEventListener('click', function () {
    view_email(singleEmail.id);
  });
  document.querySelector('#emails-view').append(email);
}

function displayEmailDetails(singleEmail) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details-view').style.display = 'block';
  document.querySelector('#email-details-view').innerHTML = `
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="d-flex w-100 justify-content-between">
            <h6 class="mb-1"><strong>From: </strong>${singleEmail.sender}</h6>
            <h6 class="mb-1"><strong>To: </strong>${singleEmail.recipients}</h6>
            <h6 class="mb-1"><strong>Subject: </strong>${singleEmail.subject}</h6>
            <small>${formatDate(singleEmail.timestamp)}</small>
          </div>
          <div class="d-flex w-100">
            <span class="mt-5">${singleEmail.body}</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

function createReplyButton(singleEmail) {
  const btn_reply = document.createElement('button');
  btn_reply.innerHTML = "Reply";
  btn_reply.className = "btn btn-primary mt-4 me-3 btn-sm";
  btn_reply.addEventListener('click', function () {
    compose_email();
    document.querySelector('#compose-recipients').value = singleEmail.sender;
    let subject = singleEmail.subject;
    if (subject.split(' ', 1)[0] != "Re:") {
      subject = "Re: " + singleEmail.subject;
    } else {
      subject = singleEmail.subject;
    }
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = `On ${singleEmail.timestamp}, ${singleEmail.sender} wrote: ${singleEmail.body}`;
  });
  return btn_reply;
}

function createArchiveButton(singleEmail) {
  // Check if email is being archive at Sent tray. If true, then return empty archive button
  if (current_mailbox === 'sent') {
    return null;
  }

  if (current_mailbox === 'inbox' || current_mailbox === 'archive') {
    const btn_archive = document.createElement('button');
    btn_archive.innerHTML = singleEmail.archived ? "Unarchive" : "Archive";
    btn_archive.className = singleEmail.archived ? "btn btn-success mt-4 btn-sm" : "btn btn-danger mt-4 btn-sm";
    btn_archive.addEventListener('click', function () {
      fetch(`/emails/${singleEmail.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !singleEmail.archived
        })
      })
        .then(() => { load_mailbox('archive') });
    });

    return btn_archive;
  }
}


function markEmailAsRead(emailId) {
  fetch(`/emails/${emailId}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  });
}
