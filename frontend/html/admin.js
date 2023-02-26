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
function formatPrice(price){
  formatter = new Intl.NumberFormat('de-AT');
  return formatter.format(price);
}
var cookie_token = getCookie('token');

const parseJwt = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
      return null;
    }
  };
  
let tokenContent = parseJwt(cookie_token);
let greeting = document.getElementById('greeting');
greeting.innerText = 'Hallo '+tokenContent.displayname
console.log(tokenContent);
if (tokenContent.admin == true){
  console.log("Hello Admin");
  let settings = document.getElementById('admin-settings');
  settings.removeAttribute('hidden');
}
