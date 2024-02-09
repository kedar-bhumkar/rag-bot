const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "https://image.flaticon.com/icons/svg/327/327779.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "User";

msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const msgText = msgerInput.value;
  if (!msgText) return;

  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  msgerInput.value = "";
  console.log("Invoking bot with msg:" + msgText)
  // Make ws call and get reesponse
  //Send resp to botResponse  
  response = invokeBot(msgText)

});

function invokeBot(msgText) {
  // Specify the endpoint URL
  const endpoint = 'http://127.0.0.1:8000/chat';

  // Create an object with the data to be sent in the request
  const data = {
    msg: msgText
  };

  console.log("POST call...")

  // Use the fetch API to send a POST request
  fetch_resp = fetch(`${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Set the content type based on your API requirements
      // Add any additional headers if needed
    },
    // Convert the data object to JSON and send it in the request body
    body: JSON.stringify(data)
  })
    .then(response => {
      // Check if the request was successful (status code 2xx)
      if (response.ok) {
        //console.log("response -" + response.json())
        //botResponse(response.json());
        return response.json(); // Parse the response body as JSON
      } else {
        //botResponse("Bot comms failure..")
        //throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }
    })
    .then(responseData => {
      // Handle the successful response data
      console.log('Response:', responseData);
      botResponse(responseData.bot_response)
    })
    .catch(error => {
      // Handle errors during the fetch operation
      console.error('Fetch error:', error);
    });

    

}


function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function botResponse(response) {
  //const r = random(0, BOT_MSGS.length - 1);
  //const msgText = BOT_MSGS[r];
  //const delay = response.split(" ").length * 100;
  const delay = 100;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", response);
  }, delay);
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}
