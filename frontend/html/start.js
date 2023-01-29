console.log("Start Javascript");
const cdpServer = "http://" + window.location.hostname + ":81/api"



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
    console.log("Show Login for User: "+ user.id + " AuthMethod = " + user.authmethod)
    // first check User AuthMethod 0 = PIN ; 1= Password; 2= 2FA, 3=TOTP Only
    if (user.authmethod == 0 || user.authmethod == 3 ){
        var pinfieldModal = new bootstrap.Modal(document.getElementById('pinfieldModal'));
        document.getElementById('pinEntry').value = "";
        pinfieldModal.toggle();
    }

   
}

function addPin(number){
    pinEntry = document.getElementById('pinEntry');
    pinEntry.value = pinEntry.value.concat(number);
    let pin = pinEntry.value;
    if (pin.length == 4 || pin.length == 6){
        //Automatic Login try:
        console.log("Automatic Login Try");
    }
}


fetch(cdpServer+'/users')
.then(response => {
    return response.json();
})
.then(users => {
    console.log(users);
    users.forEach(creatUserCard);
})