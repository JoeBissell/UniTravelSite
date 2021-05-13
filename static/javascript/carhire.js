window.onload = () => {

    // Function to create opacity slideshow on main page

    function slideShow(seconds) {
        let time = seconds * 1000;
        const progressline = document.getElementById("slideshow-progress");
        let currentSlide = document.getElementById("slideshow").getElementsByTagName("img");
        let counter = 0;

        // Set opacity every 4 seconds
        let myCounter = 1;
        let progressCounter = 1;

        setInterval(() => {

            progressCounter = progressCounter + 0.1;
            progressline.style.width = progressCounter + "%";

            if (progressCounter >= 100) {
                progressCounter = 0;
            }

            if (myCounter >= time) {
                currentSlide[counter].style.opacity = "0";
                counter++;

                if (counter == currentSlide.length) {
                    counter = 0;
                }

                currentSlide[counter].style.opacity = "1";
                myCounter = 1;
            }
          myCounter += seconds
        }, seconds)
    }


    // If pathname is main page

    if (window.location.pathname == "/joe") {
        slideShow(3);
    }
}