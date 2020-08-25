// Get all contacts
const getContacts = require('./getContacts.js'); 

//Send text by automation
const sendText = require('./sendText.js');

getContacts()
.then(res => {
    console.log(res)
    /*
        res is the object that contains 
        the whatsapp number and all details 
        to be passed to the sendText() function
    */
    sendText(res)
})
.then(err => {
    console.log(err)
})
