document.addEventListener('DOMContentLoaded', function() {
    // Your JavaScript code here

    const toastMessage = document.getElementById("toast");

    const iconContainer = document.querySelectorAll(".icon-container");
    const sideBarOverlay = document.querySelector(".comment-backdrop");
    const sideBarComponent = document.querySelector(".comment-main");
    const sideBarCloseBtn = document.querySelector(".comment-close-icon");
    const commentCount = document.querySelector(".comments");
    const showImageBtn = document.querySelector(".btn-cover");
    const showSubtitleBtn = document.querySelector(".btn-subtitle");
    const showSubtitleField = document.querySelector(".displaysub");

    var isModalOpened = false;
    console.log(isModalOpened);


    if (toastMessage) {
        console.log("here");

        toastr.options = {
            "closeButton": true,
            "debug": false,
            "newestOnTop": false,
            "progressBar": true,
            "positionClass": "toast-top-right",
            "preventDuplicates": false,
            "onclick": null,
            "showDuration": "300",
            "hideDuration": "1000",
            "timeOut": "5000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        }

        const tag = toastMessage.dataset.messageTag;
        const message = toastMessage.innerText
        switch(tag) {
            case 'success':
                toastr.success(message, tag);
                break;
            case 'info':
                toastr.info(message, tag);
                break;
            case 'warning':
                toastr.warning(message, tag);
                break;
            case 'error':
                toastr.error(message, tag);
                break;
        }
    }

    showImageBtn?.addEventListener("click", () => {
        console.log("clicked on image btn")
        showImageContainer.classList.toggle("display")
    })

    showSubtitleBtn?.addEventListener("click", () => {
        console.log("clicked on description btn")
        showSubtitleField.classList.toggle("displaysub")
    })

    const input = document.getElementById("id_image");
    const preview = document.getElementById('file-preview');
    const showImageContainer = document.querySelector(".display");

    const previewPhoto = () => {
        console.log("here")
        showImageContainer.style.display = "none";
        preview.style.display = "block";
        const file = input.files;
        console.log(file)
        if (file) {
            const fileReader = new FileReader();
            fileReader.onload = event => {
                preview.setAttribute('src', event.target.result);
            }
            fileReader.readAsDataURL(file[0]);
        }
        console.log(preview);
    }

    input?.addEventListener('change', previewPhoto);

    $(document).scroll(function() {
        var y = $(this).scrollTop();
        if (y > 20) {
            $('.blog-actions').fadeIn();
        } else {
            $('.blog-actions').fadeOut();
        }
    });

    console.log($("#likes").text());

    // if ($("#likes").text() > 0) {
    //     $(".fa-heart").removeClass('fa-regular');
    //     $(".fa-heart").addClass('fa-solid');
    //     $(".fa-heart").css('color', 'red');
    // }

    iconContainer.forEach((iconDiv) => {
        iconDiv.addEventListener("click", (e) => {
            console.log("icon container clicked");
            console.log(iconDiv);
            const icon = iconDiv.querySelector("i");
            console.log(icon);

            icon.classList.add("scale");
            icon.classList.remove("scale")
            
            if (icon.classList.contains('fa-heart')) {
                // icon.classList.remove('fa-regular');
                // icon.classList.add('fa-solid');
                // icon.style.color = 'red';
                // console.log('heart');

                const post_id = icon.dataset.blogid; 
                const csrf_token = icon.dataset.csrftoken;  

                console.log(post_id);
                console.log(csrf_token);
                console.log(icon);
                // Making the AJAX POST request
                fetch(`http://127.0.0.1:8000/blog/likepost/${post_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    },
                    body: JSON.stringify({
                        'post_id': post_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.message === 'Liked') {
                        console.log(data.message);
                        icon.classList.remove('fa-regular');
                        icon.classList.add('fa-solid');
                        icon.style.color = 'red';

                        if (data.likes_count !== undefined) {
                            // Update the likes count on the page
                            console.log($(".likes").text())
                            $("#likes").text(data.likes_count);
                        }

                    } else if (data.message === 'Already liked') {
                        icon.classList.add('fa-solid');
                        icon.style.color = 'red';
                        toastr.info("You've already Liked this post", "info");
                    } else {
                        icon.classList.remove('fa-solid');
                        icon.classList.add('fa-regular');
                        icon.style.color = 'inherit';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    console.log('An error occurred. Please try again.');
                });
                
            }

            if (icon.classList.contains('fa-comment-dots')) {
                console.log("click on comments");
                isModalOpened = true;
                console.log(isModalOpened);
                document.body.classList.add("modal-open")
                sideBarOverlay.style.display = "block";
                sideBarComponent.style.transform = "translateX(0px)";
            }
        })
    })

    sideBarCloseBtn?.addEventListener("click", () => {
        isModalOpened = false
        console.log(isModalOpened);
        document.body.classList.remove("modal-open")
        sideBarComponent.style.transform = "translateX(500px)";
        sideBarOverlay.style.display = "none"
    })

    sideBarOverlay?.addEventListener("click", () => {
        isModalOpened = false
        console.log(isModalOpened);
        document.body.classList.remove("modal-open")
        sideBarComponent.style.transform = "translateX(500px)";
        sideBarOverlay.style.display = "none"
    })
    
    const commentBtn = document.getElementById("commentBtn");
    const commentForm = document.getElementById("comments");

    commentBtn?.addEventListener("click", (e) => {
        const post_id = commentForm.dataset.blogid; 
        const csrf_token = commentForm.dataset.csrftoken;  
        const mainComment = commentForm.value;

        console.log(post_id);
        console.log(csrf_token);

        const data = {
            'comment': mainComment,
            'parent': null
        }

        fetch(`http://127.0.0.1:8000/blog/commentpost/${post_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success) {
                toastr.success("Comment created succesfully", "success");
                const newCommentHTML = `
                    <div class="post-comment">
                        <div class="post-user d-flex align-items-center justify-content-start" style="gap: 0.6rem;">
                            <img src='images/blank-profile-picture.webp' alt="profile picture" class="post-profile-img post-comment--user-img"/>
                            <div class="post-comment-user">
                                <p class="post-user--username">${data.comment_author}</p>
                                <p class="comment-date">${data.comment_date}</P>
                            </div>
                        </div>

                        <div class="post-main">
                            ${data.comment_text}
                        </div>

                        <div class="post-actions d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                            <div class="d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                                <div>
                                    <i class="fa-regular fa-heart icon"></i>
                                    <span>0</span>
                                </div>
                                ${data.comment?.replies?.count ? `<div>
                                    <i class="fa-regular fa-comment-dots icon"></i>
                                    <span>${data.comment?.replies?.count || 0} </span>
                                </div>
                                <button type="button" class="reply-link" id="show-replies">Show Replies</button>`: "" } 
                            </div>
                            <button type="button" class="reply-link" id="reply-link">Reply</button>
                        </div>

                        
                        <div class="reply-comment-form d-none" id="reply-comment-form">
                            <span class="vline"></span>
                            <div class="post-user d-flex align-items-center justify-content-start" style="gap: 0.6rem;">
                                <img src="{% static 'images/blank-profile-picture.webp' %}" alt="profile picture" class="post-profile-img"/>
                                <p class="post-reply-user--username">Wisdom Elue</p>
                            </div>
                            <form method="post" autocomplete="off" name="form" style="text-align: left;">
                                {% csrf_token %}
                                <textarea id="replies" name="replies" placeholder="Write a Reply"></textarea>
                                <div class="d-flex align-items-center justify-content-start" style="gap: 1rem;">
                                    <button type="button" class="btn btn-outline-dark" id="cancelBtn">Cancel</button>
                                    <button type="submit" class="btn btn-dark" id="replyBtn">Reply</button>
                                </div>
                            </form>
                        </div>

                        <div class="reply-comment d-none" id="reply-comment">
                        {% if comment.replies.exists %}
                                <span class="vline"></span>
                                {% for replies in comment.replies.all %}
                                    <div class="post-user d-flex align-items-center justify-content-start" style="gap: 0.6rem;">
                                        <img src="{% static 'images/blank-profile-picture.webp' %}" alt="profile picture" class="post-profile-img post-comment--user-img"/>
                                        <div class="post-comment-user">
                                            <p class="post-user--username">{{replies.author.username}}</p>
                                            <p class="comment-date">{{replies.created_at}}</P>
                                        </div>
                                    </div>
            
                                    <div class="post-main">
                                        {{ replies.comment }} 
                                    </div>
            
                                    <div class="post-actions d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                                        <div class="d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                                            <div>
                                                <i class="fa-regular fa-heart icon"></i>
                                                <span>0</span>
                                            </div>
                                            {% if replies.comment.exists %}
                                                <div>
                                                    <i class="fa-regular fa-comment-dots icon"></i>
                                                    <span>1</span>
                                                </div>
                                                <button type="button" class="reply-link">Hide Replies</button>
                                            {% endif %}
                                        </div>
                                        <button type="button" class="reply-link">Reply</button>
                                        </div>
                                {% endfor %}
                            {% endif %}
                        </div>
                    </div>
                `
                $("#comments-empty").addClass("d-none");
                document.getElementById("comments").value = "";
                document.querySelector('.comment-body').insertAdjacentHTML('afterbegin', newCommentHTML);
            }
        })

    })

    const replyBtn = document.querySelectorAll("#replyBtn");

    replyBtn.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();  // Prevent the default form submission

            const repliesForm = button.closest(".reply-comment-form");
            repliesForm.style.display = "none"
            const post_id = repliesForm.querySelector("textarea").dataset.blogid; 
            const csrf_token = repliesForm.querySelector("textarea").dataset.csrftoken;  
            const mainComment = repliesForm.querySelector("textarea").value;
            const parentComment = repliesForm.querySelector("textarea").dataset.parentid;

    
            console.log(post_id);
            console.log(csrf_token);
            console.log(parentComment)
            console.log(mainComment);
    
            const data = {
                'comment': mainComment,
                'parent': parentComment
            }
    
            fetch(`http://127.0.0.1:8000/blog/commentpost/${post_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                    toastr.success("Comment created successfully", "success");
                    $(".reply-comment").removeClass("d-none")
                    const newCommentHTML = `
                    <div class="replies-text">
                        <div class="post-user d-flex align-items-center justify-content-start" style="gap: 0.6rem;">
                            <img src="{% static 'images/blank-profile-picture.webp' %}" alt="profile picture" class="post-profile-img post-comment--user-img"/>
                            <div class="post-comment-user">
                                <p class="post-user--username">${data.comment_author}</p>
                                <p class="comment-date">${data.comment_date}</P>
                            </div>
                        </div>
    
                        <div class="post-main">
                            ${data.comment_text}
                        </div>
    
                        <div class="post-actions d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                            <div class="d-flex align-items-center justify-content-start" style="gap: 0.7rem;">
                                <div>
                                    <i class="fa-regular fa-heart icon"></i>
                                    <span>0</span>
                                </div>
                            </div>
                            <button type="button" class="reply-link">Reply</button>
                        </div>
                    </div>`
    
                    document.querySelector(".replies-comment").innerHTML = newCommentHTML;
                }
            })
    
        })
    })

    const commentLikeBtn = document.querySelectorAll(".comment-like-icon")

    commentLikeBtn.forEach((iconDiv) => {
        iconDiv.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("Here comment like btn")
            icon = iconDiv.querySelector("i");
            console.log(icon)

            if (icon.classList.contains('fa-heart')) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid');
                icon.style.color = 'red';
                console.log('heart');

                const comment_id = icon.dataset.commentid; 
                const csrf_token = icon.dataset.csrftoken;  
                const post_id = icon.dataset.blogid;  

                console.log(comment_id);
                console.log(csrf_token);
                console.log(post_id);
                console.log(icon);
                // Making the AJAX POST request
                fetch(`http://127.0.0.1:8000/blog/likecomment/${post_id}/${comment_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token
                    },
                    body: JSON.stringify({
                        'post_id': post_id,
                        'comment_id': comment_id
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.message === 'Liked') {
                        console.log(data.message);
                        icon.classList.remove('fa-regular');
                        icon.classList.add('fa-solid');
                        icon.style.color = 'red';

                        if (data.likes_count !== undefined) {
                            // Update the likes count on the page
                            console.log($(".comment-like-count").text())
                            icon.nextElementSibling.textContent = data.likes_count;
                            //$(".comment-like-count").text(data.likes_count);
                        }

                    } else if (data.message === 'Already liked') {
                        icon.classList.add('fa-solid');
                        icon.style.color = 'red';
                        toastr.info("You've already Liked this post", "info");
                    } else {
                        icon.classList.remove('fa-solid');
                        icon.classList.add('fa-regular');
                        icon.style.color = 'inherit';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    console.log('An error occurred. Please try again.');
                    toastr.error(error, "error");
                });
                
            }
        })
    })


    $(document).on("ready", function() {
        $("#logbtn").on("click", function() {
            console.log("Hello from jquery!");
        })

    })

    let isMouseOverProfile = false;

    $(".author").hover(
        function() {
            console.log("mouseover");
            $(this).siblings(".profileContainer").removeClass("d-none");
        },
        function() {
            console.log("mouseout");
            const profileContainer = $(this).siblings(".profileContainer");

            setTimeout(() => {
                if (!isMouseOverProfile) {
                    profileContainer.addClass("d-none");
                }
            }, 100); // Short delay to allow for mouse enter
        }
    );

    $(".profileContainer").on("mouseenter", function() {
        console.log("mouse enter");
        isMouseOverProfile = true;
        $(this).removeClass("d-none");
    });

    $(".profileContainer").on("mouseleave", function() {
        console.log("mouse leave");
        isMouseOverProfile = false;
        $(this).addClass("d-none");
    });

    textarea = document.querySelector("#comments");
    textarea?.addEventListener('input', autoResize, false);

    function autoResize() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    }

    $(".show-replies").each(function() {
        $(this).click(function() {
            console.log("show replies");
            const button = $(this);
            const replyComment = button.closest(".post-comment").find(".reply-comment");
            
            if (button.text() === "Show Replies") {
                button.text("Hide Replies");
            } else {
                button.text("Show Replies");
            }
            
            replyComment.toggleClass("d-none");
        });
    });
    
    $(".reply-link").each(function() {
        $(this).click(function() {
            console.log("reply link");
            const button = $(this);
            const replyCommentForm = button.closest(".post-comment").find(".reply-comment-form");


            replyCommentForm.toggleClass("d-none");
        });
    });

    $("#cancelBtn").click(() => {
        $("#reply-comment-form").addClass("d-none");
    })

    $("#themeBtn").click(function() {
        if ($("#themeBtn i").hasClass("fa-moon")) {
            $("#themeBtn i").removeClass("fa-moon");
            $("#themeBtn i").addClass("fa-sun");
        } else {
            $("#themeBtn i").removeClass("fa-sun");
            $("#themeBtn i").addClass("fa-moon");
        }
    })
});




