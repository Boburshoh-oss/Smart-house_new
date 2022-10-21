
const client = new WebSocket('wss://'
+ window.location.host
+ '/ws'
+ '/')

const view = document.getElementById("stream");


function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }


client.onmessage = function (event) {
    const { data } = event
    const frame = JSON.parse(data).message
    // console.log(frame)
    if (frame instanceof Blob) {
        var urlObject = URL.createObjectURL(frame);
        view.src = urlObject;
      }
}

function sendMessage(){
    // console.log("message is sending")
    client.send("on")

}
