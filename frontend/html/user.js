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


function createProductCard(product) {
  console.log(product);
  let btnGroup = document.createElement('div');
  btnGroup.className='btn-group';
  btnGroup.role='group';
  btnGroup.style='width:100%';

  let btn1 = document.createElement('button');
  btn1.type='button';
  btn1.className='btn btn-lg btn-primary btn-block';
  btn1.innerHTML='<img src="icons/basket.svg">';

  let btn2 = document.createElement('button');
  btn2.type='button';
  btn2.className='btn btn-lg btn-primary btn-block';
  btn2.innerHTML='<img src="icons/send.svg">';

  btnGroup.appendChild(btn1);
  btnGroup.appendChild(btn2);

  
  let cardSubTitle = document.createElement('h6');
  cardSubTitle.className = 'card-subtitle mb-2 text-muted'
  cardSubTitle.innerText = formatPrice(product.price/100) + " €";
  let cardTitle = document.createElement('h5');
  cardTitle.className = 'card-title';
  cardTitle.innerText = product.productname;

  let cardImage = document.createElement('img');
  cardImage.className="card-img-top";
  cardImage.style="width:50%";
  cardImage.src= 'icons/cup-hot-fill.svg';
  

  let cardBody = document.createElement('div');
  cardBody.className = 'card-body';
  cardBody.appendChild(cardImage);
  cardBody.appendChild(cardTitle);
  cardBody.appendChild(cardSubTitle);
  cardBody.appendChild(btnGroup);

  let card = document.createElement('div');
  card.className = 'card shadow cursor-pointer';
  card.appendChild(cardBody);


  let prodcol = document.createElement('div');
  prodcol.className = 'col-sm-2 my-1';
  prodcol.appendChild(card);

  let productList = document.getElementById('products');
  productList.appendChild(prodcol);


}

fetch(cdpServer + '/products')
    .then(response => {
      return response.json();
    })
    .then(products => {
      console.log(products);
      products.forEach(product => {
        if (product.active) {
          createProductCard(product);
        }
      });
    })