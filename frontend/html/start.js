console.log("Start Javascript");
const cdpServer = "https://" + window.location.hostname + "/api"


function setCookie(cname, cvalue, exmin) {
    const d = new Date();
    d.setTime(d.getTime() + (exmin * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";SameSite=Strict";
  }

function getCookie(cname){
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}
function creatUserCard(user){
    let userlist = document.getElementById('userlist');

    let collection = document.createElement('div');
    collection.className = 'col';

    let usercard = document.createElement('div');
    usercard.className = 'card h-100 shadow cursor-pointer';
    usercard.addEventListener("click", e => {
        showLogin(user);
    })
    
    let cardbody = document.createElement('div');
    cardbody.className = 'card-body';

    let cardtitle = document.createElement('div');
    cardtitle.innerText = user.displayname;
    cardtitle.className = 'card-title';



    cardbody.appendChild(cardtitle);
    usercard.appendChild(cardbody);
    collection.appendChild(usercard);
    userlist.appendChild(collection);

}

function showLogin(user){
    let pwWrong = document.getElementById('pwWrong');
    pwWrong.hidden = true;
    console.log("Show Login for User: "+ user.id + " AuthMethod = " + user.authmethod)
    // first check User AuthMethod 0 = PIN ; 1= Password; 2= 2FA, 3=TOTP Only
    if (user.authmethod == 0 || user.authmethod == 3 ){
        var pinfieldModal = new bootstrap.Modal(document.getElementById('pinfieldModal'));
        document.getElementById('pinEntry').value = "";
        pinfieldModal.toggle();
    }
    setCookie("uid",user.id,10);
    setCookie("user",user.username,10);
    setCookie("authmethod",user.authmethod,10);
   
}

function addPin(number){
    pinEntry = document.getElementById('pinEntry');
    pinEntry.value = pinEntry.value.concat(number);
    let pin = pinEntry.value;
    if (pin.length == 4 || pin.length == 6){
        //Automatic Login try:
        console.log("Automatic Login Try");
        login(getCookie("user"),pin,pin,true);

    }
}
function backspacePin(){
    pinEntry = document.getElementById('pinEntry');
    let pin = pinEntry.value;
    pinEntry.value = pin.substring(0,pin.length-1);
}
function pinChanged(){
    let pin = pinEntry.value;
    if (pin.length == 4 || pin.length == 6){
        //Automatic Login try:
        console.log("Automatic Login Try");
        login(getCookie("user"),pin,pin,true);

    }
}

function btnclick_login(){
    pinEntry = document.getElementById('pinEntry');
    let pin = pinEntry.value;
    login(getCookie("user"),pin,pin,false);
}

function login(user,pin,totp,auto){
    console.log("Automatic status: " + auto)
    let bodydata = JSON.stringify({username:user,password:pin});
    console.log(bodydata);
    fetch(cdpServer+'/login',{
        method: 'POST',
        headers: {
            'Accept':'application/json',
            'Content-Type': 'application/json'
        },
        body: bodydata
    })
    .then(response => {
        if (response.status == 401 && !auto){
            let pwWrong = document.getElementById('pwWrong');
            pwWrong.hidden = false;
            message = document.createElement('div');
            message.className = 'alert alert-danger';
            message.role = 'alert';
            message.innerText = 'Username oder Passwort falsch';
            pwWrong.appendChild(message);
            
        }
        return response.json();
    })
    .then(resp => {
        if (resp.token){
            setCookie("token",resp.token,5);
            window.location.href = '/user.html';
        }else{
            console.log(resp);
        }
    })

}
fetch(cdpServer+'/users')
.then(response => {
    return response.json();
})
.then(users => {
    console.log(users);
    users.forEach(user =>{
        if (user.favorite){
            creatUserCard(user);
        }});
    // Create a "Dummy User for others"
    var user = {"displayname":"Anderer Benutzer", "authmethod":4};
    creatUserCard(user);
})







