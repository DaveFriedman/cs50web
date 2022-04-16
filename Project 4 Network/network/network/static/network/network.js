document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".follow-button ")?.addEventListener("click", follow_profile, false);
  document.querySelectorAll(".edit-button").forEach(e => e.addEventListener("click", edit_post, false));
  document.querySelectorAll(".like-button").forEach(e => e.addEventListener("click", like_post, false));
  document.querySelectorAll(".dislike-button").forEach(e => e.addEventListener("click", dislike_post, false));

  // Autofocus textarea when create-post modal pops up
  $(document).on("shown.bs.modal", function () {
    $("#id_body").focus();
  });

  // Enable Bootstrap tooltips for timestamps
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

});


function edit_post() {
  postid = this.dataset.id;

  postbody = document.querySelector(`#post-body-${postid}`);
  posttext = document.querySelector(`#post-body-${postid}`).innerText;
  postbody.setAttribute("data-posttext",`${posttext}` );

  postfooter = document.querySelector(`#post-footer-${postid}`);
  csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  form = `
      <form id="edit-post" name="edit-post" onsubmit="update_post(${postid})">
          <input type="hidden" name="csrfmiddlewaretoken" value="${csrf}"></input>
          <div id="div_id_body" class="form-group">
              <div>
                  <textarea id="edit-textarea-${postid}" name="body" class="textarea-edit form-control"
                  cols="40" rows="6" maxlength="280" required="">${posttext}</textarea>
              </div>
          </div>
          <div class="btn-group" role="group">
              <button id="edit-post-submit-${postid}" type="submit" class="btn btn-success">Update</button>
              <button id="edit-post-cancel-${postid}" type="button" onclick="display_post(${postid})" class="btn btn-secondary">Cancel</button>
          </div>
      </form>`;

  postfooter.className = "d-none";
  postbody.innerHTML = form;
};


function update_post(postid) {
  event.preventDefault()
  post_body_update = document.querySelector(`#edit-textarea-${postid}`).value;
  csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

  fetch(`/p/${postid}/edit`, {
    method: 'POST',
    mode: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(post_body_update),
  })
  .then(response => response.json())
  .then(data => {
    display_post(data.postid, data.postbody, data.postedited);
  })
  .catch(error => console.log("update_post() error:", error));
};


function display_post(postid, body=null, edited=null) {
  postbody = document.querySelector(`#post-body-${postid}`);

  if (edited === null) {
    postbody.innerText = postbody.dataset.posttext;
  } else {
    postbody.innerText = body;

    postedited = document.querySelector(`#post-edited-${postid}`)
    postedited.outerHTML = `<span id="post-edited-${postid}"
                              class="text-black-50 time"
                              data-toggle="tooltip"
                              data-placement="top"
                              title=""
                              data-original-title="${edited}">
                                Updated just now.
                            </span>`;
    $(function () {
      $('[data-toggle="tooltip"]').tooltip();
    });
  }

  postfooter = document.querySelector(`#post-footer-${postid}`);
  postfooter.className = "mx-2 mt-2 p-2 d-flex justify-content-between";
  return false;
};


 // Follow and unfollow creators
 function follow_profile() {
  fetch(`/follow/${this.dataset.id}`)

  .then(response => response.json())
  .then(data => {
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
  .catch(error => console.log("follow() error:", error));
};


// Like and unlike posts
function like_post() {
  like_count = parseInt(document.querySelector(`#like-count-${this.dataset.id}`).innerHTML);
  fetch(`/p/${this.dataset.id}/like`)

  .then(response => response.json())
  .then(data => {
    if (data.is_liker === true) {
      document.querySelector(`#like-image-${this.dataset.id}`).className = "bi bi-heart-fill";
      document.querySelector(`#like-count-${this.dataset.id}`).innerHTML = like_count+1;
    }
    else {
      document.querySelector(`#like-image-${this.dataset.id}`).className = "bi bi-heart";
      document.querySelector(`#like-count-${this.dataset.id}`).innerHTML = like_count-1;
    }
  })
  .catch(error => console.log("like_post() error:", error));
};


// Dislike and un-dislike posts
function dislike_post() {
  dislike_count = parseInt(document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML);
  fetch(`/p/${this.dataset.id}/dislike`)

  .then(response => response.json())
  .then(data => {
    if (data.is_disliker === true) {
      document.querySelector(`#dislike-image-${this.dataset.id}`).className = "bi bi-emoji-angry-fill";
      document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML = dislike_count+1;
    }
    else {
      document.querySelector(`#dislike-image-${this.dataset.id}`).className = "bi bi-emoji-angry";
      document.querySelector(`#dislike-count-${this.dataset.id}`).innerHTML = dislike_count-1;
    }
  })
  .catch(error => console.log("dislike_post() error:", error));
};