// this module contains javascript logic for the checkout page

if(shipping == 'False'){
    //hide shipping info if the product does not require shipping
    document.getElementById('shipping-info').innerHTML = ''
}

if(user != 'AnonymousUser'){
    //hide user info input if the user is loggedin
    document.getElementById('user-info').innerHTML = ''
}

if(user != 'AnonymousUser' && shipping == 'False'){
    //hide the whole form wrapper if user is not logged in and shipping is false
    document.getElementById('form-wrapper').innerHTML = ''

    //show payment info is the user wants to buy an item that does not require shipping
    document.getElementById('payment-info').classList.remove('hidden')
}

var form = document.getElementById('form')

form.addEventListener('submit', function(e){
    //stop the form from acting upon submit
    e.preventDefault()
    console.log('form submitted...')
    // add the hidden class to the element with a class of form-button
    document.getElementById('form-button').classList.add('hidden')
    // remove the hidden class from the element with a class of payment-info
    document.getElementById('payment-info').classList.remove('hidden')
})

document.getElementById('make-payment').addEventListener('click', function(e){
    submitFormData()
})

function submitFormData(){
    //this function defines what happens when the make payment button is clicked
    console.log('payment button clicked ...')

    var userFormData = {
        // this object contains info about the user
        'first_name': null,
        'last_name': null,
        'email': null,
        'phonenumber': null,
        'total': total,
    }

    var shippingInfo = {
        // this object contains info about the shipping address
        'address': null,
        'city': null,
        'state': null,
        'zipcode': null,
        'country': null,
    }

    if(shipping != 'False'){
        // this statement sets the value of shipping info
        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.state = form.state.value
        shippingInfo.zipcode = form.zipcode.value
        shippingInfo.country = form.country.value
    }

    if(user == 'AnonymousUser'){
        // this statement sets the value user information for anonymous users
        userFormData.first_name = form.first_name.value
        userFormData.last_name = form.last_name.value
        userFormData.phonenumber = form.phonenumber.value
        userFormData.email = form.email.value
    }

    //console.log('user info: ', userFormData)
    //console.log('shipping address: ', shippingInfo)

    // The fetch API to send payment and shipping data to backend
    // define the target  url
    var url = '/process_order/'

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
        body : JSON.stringify({ 'form' : userFormData, 'shipping': shippingInfo})
    })

    // return a promise from fetch, and turn into json value
    .then((response) => response.json())

        //return data
    .then((data) => {
        console.log('success:', data);
        alert('Transaction completed');
        window.location.replace(" /store/ ")
    })
}