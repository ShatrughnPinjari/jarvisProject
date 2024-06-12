let marker = document.querySelector('#marker');
let item = document.querySelectorAll("nav a");
let audio = document.getElementById("audio");
let content = document.getElementById("content");
let userInput = document.getElementById("userInput");
let submitBtn = document.getElementById("submitBtn");
let responseContainer = document.getElementById("responseContainer");

console.log('Script loaded');

function handleSubmit() {
    let command = userInput.value.trim();
    if (command !== "") {
        console.log('User command:', command);
        responseContainer.innerHTML += `<p>User: ${command}</p>`;
        sendCommand(command); // Send the command to the backend
        userInput.value = ""; // Clear the input field
    }
}

submitBtn.addEventListener("click", handleSubmit);

userInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        handleSubmit();
    }
});

function handleVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function (event) {
        const speechResult = event.results[0][0].transcript;
        userInput.value = speechResult;
        recognition.stop();
    };
}

// document.getElementById("voiceBtn").addEventListener("click", handleVoiceInput);
voiceBtn.addEventListener("click", handleVoiceInput);

document.addEventListener("DOMContentLoaded", function () {
    const marker = document.getElementById("marker");
    const navigationLinks = document.querySelectorAll(".navigation a");

    function setCurrentPage() {
        const currentPage = window.location.pathname.split("/").pop();
        navigationLinks.forEach((link) => {
            if (link.getAttribute("href") === currentPage) {
                marker.style.left = link.offsetLeft + "px";
                marker.style.width = link.offsetWidth + "px";
            }
        });
    }

    setCurrentPage();

    navigationLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            marker.style.left = e.target.offsetLeft + "px";
            marker.style.width = e.target.offsetWidth + "px";
        });
    });
});

async function get_response() {
     console.log("we are sending your data");
    
    // Example data to send
     const dataToSend = {
     command: "tell me a joke",
     };
    
     const csrftoken = getCookie("csrftoken");
     // Backend endpoint URL
     const url = "http://127.0.0.1:8000/listen_to_frontend/";
     // Fetch request options
     const options = {
     method: "POST", // Method for sending data
     headers: {
     "Content-Type": "application/json", // Specify content type as JSON
 "X-CSRFToken": csrftoken,
     },
     body: JSON.stringify(dataToSend), // Convert data to JSON string
     };
     // Send the HTTP request
     fetch(url, options)
     .then((response) => {
     if (!response.ok) {
     throw new Error("Network response was not ok");
     }
     return response.json(); // Parse response JSON
     })
     .then((data) => {
     console.log("Response from backend:", data);
    // Do something with the response data
     })
     .catch((error) => {
     console.error("Error sending data to backend:", error);
     });
    }
    
    function getCookie(name) {
     let cookieValue = null;
     if (document.cookie && document.cookie !== "") {
   const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
     const cookie = cookies[i].trim();
   if (cookie.substring(0, name.length + 1) === name + "=") {
     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
     break;
    }
     }
     }
     return cookieValue;
    }
    
    function startRecording() {
    navigator.mediaDevices
     .getUserMedia({ audio: true })
      .then(function (stream) {
   let mediaRecorder = new MediaRecorder(stream);
     let chunks = [];
    
     mediaRecorder.ondataavailable = function (e) {
     chunks.push(e.data);
     };
    
     mediaRecorder.onstop = function (e) {
     let blob = new Blob(chunks, { type: "audio/wav" });
     console.log(blob);
     sendAudio(blob);
     };
     //         let csrftoken = getCookie('csrftoken');
     // console.log(csrftoken)
    
    mediaRecorder.start();
     setTimeout(function () {
     mediaRecorder.stop();
     }, 5000); // Record for 5 seconds
     })
     .catch(function (err) {
     console.log("The following getUserMedia error occurred: " + err);
     });
    }
    
    function sendAudio(blob) {
    let formData = new FormData();
     formData.append("blob", blob);
    
     var blobUrl = URL.createObjectURL(blob);
    
    console.log(formData.get("blob"));

    fetch("http://127.0.0.1:8000/listen_to_frontend/", {
     method: "POST",
     body: formData,
     })
     .then((response) => response.json())
    .then((data) => {
     console.log("Response from server:", data);
     })
     .catch((error) => {
     console.error("Error sending audio to server:", error);
     });
    }