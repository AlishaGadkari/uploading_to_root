document.addEventListener('DOMContentLoaded', function () {
    const popupOverlay = document.getElementById('popupOverlay');
    const openFormButton = document.getElementById('openFormButton');
    const closePopup = document.getElementById('closePopup');

    // Function to open the popup
    openFormButton.addEventListener('click', function () {
        popupOverlay.style.display = 'block';
    });

    // Function to close the popup
    closePopup.addEventListener('click', function () {
        popupOverlay.style.display = 'none';
    });

    // Close the popup when clicking outside of the popup content
    popupOverlay.addEventListener('click', function (event) {
        if (event.target === popupOverlay) {
            popupOverlay.style.display = 'none';
        }
    });
});