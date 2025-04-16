/*================<< Header menu js start here>>====================*/

const menu = document.querySelector('.menu');
const menuSection = menu.querySelector('.menu-section');
const menuArrow = menu.querySelector('.menu-mobile-arrow');
const menuClosed = menu.querySelector('.menu-mobile-close');
const menuTrigger = document.querySelector('.menu-mobile-trigger');
const menuOverlay = document.querySelector('.header__overlay');
let subMenu;




menuSection.addEventListener('click', (e) => {
  if (!menu.classList.contains('active')) {
    return;
  }

  if (e.target.closest('.menu-item-has-children')) {
    const hasChildren = e.target.closest('.menu-item-has-children');
    showSubMenu(hasChildren);
  }


});

menuArrow.addEventListener('click', () => {
  hideSubMenu();
});

menuTrigger.addEventListener('click', () => {
  toggleMenu();
});

menuClosed.addEventListener('click', () => {
  toggleMenu();
});

menuOverlay.addEventListener('click', () => {
  toggleMenu();
});

function toggleMenu() {
  menu.classList.toggle('active');
  menuOverlay.classList.toggle('active');
}



function showSubMenu(hasChildren) {
  subMenu = hasChildren.querySelector('.submenu');
  subMenu.classList.add('active');
  subMenu.style.animation = 'slideLeft 0.5s ease forwards';
  const menuTitle = hasChildren.querySelector('i,svg').parentNode.childNodes[0].textContent;
  menu.querySelector('.menu-mobile-title').innerHTML = menuTitle;
  menu.querySelector('.menu-mobile-header').classList.add('active');

  // Check for nested submenu-child elements
  const nestedSubmenuChild = subMenu.querySelector('.submenu-child');
  if (nestedSubmenuChild) {
    showNestedSubmenuChild(nestedSubmenuChild);
  }
}

function showNestedSubmenuChild(nestedSubmenuChild) {
  nestedSubmenuChild.classList.add('active');
  nestedSubmenuChild.style.animation = 'slideLeft 0.5s ease forwards';

  // Recursive call for further nested submenus
  const nestedSubmenu = nestedSubmenuChild.querySelector('.submenu');
  if (nestedSubmenu) {
    showNestedSubmenuChild(nestedSubmenu.querySelector('.submenu-child'));
  }
}




function hideSubMenu() {
  subMenu.style.animation = 'slideRight 0.5s ease forwards';
  setTimeout(() => {
    subMenu.classList.remove('active');
  }, 300);

  menu.querySelector('.menu-mobile-title').innerHTML = '';
  menu.querySelector('.menu-mobile-header').classList.remove('active');
}



// Function to adjust the position of the last submenu-child
function adjustLastSubmenuChildPosition() {
  const lastMenuItem = document.querySelector('.menu > ul > li:last-child');
  if (lastMenuItem) {
    const lastSubmenuChild = lastMenuItem.querySelector('.submenu-child');
    if (lastSubmenuChild) {
      // Calculate the left position to shift the submenu-child
      const shiftLeft = 250; // Adjust the value according to your needs
      lastSubmenuChild.style.left = `-${shiftLeft}px`;
    }
  }
}

window.onresize = function () {
  if (this.innerWidth > 1199) {
    // Close the menu if it's active
    if (menu.classList.contains('active')) {
      toggleMenu();
    }

    // Adjust the position of the last submenu-child
    adjustLastSubmenuChildPosition();
  }
};



// Function to make the header sticky on scroll with animation
function makeHeaderSticky() {
  const headerBottom = document.querySelector('.header');
  const headerBottomOffset = headerBottom.offsetTop + headerBottom.offsetHeight;

  window.addEventListener('scroll', () => {
    if (window.pageYOffset >= headerBottomOffset) {
      headerBottom.classList.add('fixed');
    } else {
      headerBottom.classList.remove('fixed');
    }
  });
}
// Call the function to make the header sticky
makeHeaderSticky();



/*================<< Header menu js end here>>====================*/




/*================<< Searchbar js start here>>====================*/

document.addEventListener("DOMContentLoaded", function () {
  const searchIcon = document.querySelector(".search-icon");
  const searchForm = document.querySelector(".trk-search");
  const overlay = document.querySelector(".trk-search__overlay");

  searchIcon.addEventListener("click", function () {
    searchForm.classList.add("active");
    overlay.style.display = "block";
  });

  overlay.addEventListener("click", function () {
    searchForm.classList.remove("active");
    overlay.style.display = "none";
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && searchForm.classList.contains("active")) {
      searchForm.classList.remove("active");
      overlay.style.display = "none";
    }
  });
});

/*================<< Searchbar js end here>>====================*/