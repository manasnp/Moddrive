const menuButton = document.querySelector("[data-menu-button]");
const navigationMenu = document.querySelector("[data-menu]");

if (menuButton && navigationMenu) {
    menuButton.addEventListener("click", function () {
        const menuIsOpen = navigationMenu.classList.toggle("open");

        menuButton.setAttribute(
            "aria-expanded",
            menuIsOpen.toString()
        );
    });

    navigationMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navigationMenu.classList.remove("open");
            menuButton.setAttribute("aria-expanded", "false");
        });
    });
}