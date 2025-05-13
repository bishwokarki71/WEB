
document.addEventListener('DOMContentLoaded', function () {
    // Check if the user is logged in when the page is loaded
    checkLoginStatus();
    fetch('/check_logged_in')  // Send a request to check login status
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                // If not logged in, redirect to login page
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.log('Error checking login status:', error);
            window.location.href = '/login'; // Redirect if there was an error checking
        });
    
    // Handling the back button event
    window.addEventListener("popstate", function () {
        // Force logout if the user navigates back
        window.location.href = '/login';
    });
    
    // Your existing functionality here...
    const febHolidays = [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      


     
    
    ];
    
    const ulEl = document.querySelector("ul");
    const d = new Date();
    let daynumber = d.getMonth() == 1 ? d.getDate() - 1 : 0;
    let activeIndex = daynumber;
    const rotate = -360 / febHolidays.length;
    init();
    
    function init() {
        febHolidays.forEach((holiday, idx) => {
            const liEl = document.createElement("li");
            liEl.style.setProperty("--day_idx", idx);
            liEl.innerHTML = `<time datetime="2022-02-${idx + 1}">${idx + 1}</time><span>${holiday}</span>`;
            ulEl.append(liEl);
        });
        ulEl.style.setProperty("--rotateDegrees", rotate);
        adjustDay(0);
    }

    function adjustDay(nr) {
        daynumber += nr;
        ulEl.style.setProperty("--currentDay", daynumber);
        const activeEl = document.querySelector("li.active");
        if (activeEl) activeEl.classList.remove("active");
        activeIndex = (activeIndex + nr + febHolidays.length) % febHolidays.length;
        const newActiveEl = document.querySelector(`li:nth-child(${activeIndex + 1})`);
        document.body.style.backgroundColor = window.getComputedStyle(newActiveEl).backgroundColor;
        newActiveEl.classList.add("active");
    }

    function checkLoginStatus() {
    fetch('/check_logged_in')  // Send GET request to check login status
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {
            if (!data.logged_in) {  // If user is not logged in
                window.location.href = "/login";  // Redirect to login page
            }
        })
        .catch(error => {
            console.error("Error checking login status:", error);
        });
}

// Call this function when the page loads to verify login status
checkLoginStatus();

    window.addEventListener("keydown", (e) => {
        switch (e.key) {
            case "ArrowUp":
                adjustDay(-1);
                break;
            case "ArrowDown":
                adjustDay(1);
                break;
            default:
                return;
        }
    });

    let scrollTimeout = null;

    window.addEventListener("wheel", (e) => {
        if (scrollTimeout) return; // If waiting, ignore new scroll

        if (e.deltaY < 0) {
            adjustDay(-1); // Scroll up
        } else if (e.deltaY > 0) {
            adjustDay(1); // Scroll down
        }

        scrollTimeout = setTimeout(() => {
            scrollTimeout = null;
        }, 300); // Adjust the delay as needed
    });
});
