const url = `ws://192.168.10.229:9876`
const client = new WebSocket(url)

const view = document.getElementById("stream");


function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
  }


client.onmessage = function(event) {
    const {data} = event
    if (data instanceof Blob) {
        var urlObject = URL.createObjectURL(data);
        view.src = urlObject;
      }
}

function sendMessage(){
    console.log("message is sending")
    client.send("on")

}
