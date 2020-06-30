//store all elements with the 'update-cart' class name in the 'updateBtns' variable 
var updateBtns = document.getElementsByClassName('update-cart') 

//loop through the 'updateBtns' variable 
for(var i = 0; i < updateBtns.length; i++){
    //add event listener on click for each button, and activate a function
    updateBtns[i].addEventListener('click', function(){
        //get product id associated with the button
        var productId = this.dataset.product
        //get product id associated with the button
        var action = this.dataset.action
        //console.log('productId:', productId, 'action:', action)
        //console.log('user:', user)

        //check if user is authenticated or not
        if(user === 'AnonymousUser'){
           // console.log('not logged in')
            updateUserOrder(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    // this function sends api data to the updateItem view
   // console.log('User is logged in. Sending data...')

    // send data to the url
    var url = '/update_item/'

    // fetch takes two parameters. Url to fetch to and the data type
    fetch(url, {
        // define the data to be sent
        method : 'POST',
        //define headers
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        //define the body
        body : JSON.stringify({'productId': productId, 'action': action})
    })

    // return a promise from fetch, and turn into json value
    .then((response) => {
        return response.json()
    })

        //return data
    .then((data) => {
       // console.log('data:', data)
        location.reload()
    })
}