const followLinks = document.querySelectorAll(".follow-user");
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("follow-user")) {
        e.preventDefault();
        const followLink = e.target;
        const username = followLink.getAttribute("data-follow-username");
        const flag = followLink.textContent;
        const api_endpoint = `/follow/${username}/${flag}/`;
        fetch(api_endpoint)
            .then(response => response.json())
            .then(data => {
            followLink.textContent = followLink.textContent === "follow" ? "unfollow" : "follow";
        });
    }
});