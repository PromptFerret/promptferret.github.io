document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("img").forEach((image) => {
        // Create the copy button
        let button = document.createElement("button");
        button.className = "copy-image-button";
        button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 1 2 2v1"></path>
        </svg>`;

        // Wrap the image in a div for better positioning
        let wrapper = document.createElement("div");
        wrapper.className = "image-container";
        image.parentNode.insertBefore(wrapper, image);
        wrapper.appendChild(image);
        wrapper.appendChild(button);

        // Handle copy event
        button.addEventListener("click", () => {
            let imageUrl = image.src; // Get full image URL
            navigator.clipboard.writeText(imageUrl).then(() => {
                button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>`; // Change to checkmark icon

                setTimeout(() => {
                    button.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 1 2 2v1"></path>
                    </svg>`; // Reset back to copy icon
                }, 2000);
            });
        });
    });
});
