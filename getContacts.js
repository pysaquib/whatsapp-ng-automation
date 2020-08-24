module.exports = async function getContacts() {
    const axios = require('axios');
    let contacts = {}
    await axios.get('https://sheetdb.io/api/v1/dlk07s7isr190')
        .then((res) => {
            // console.log(res.data);
            contacts = res.data;
        })
        .catch(err => {
            console.log(err)
        });
    return contacts;
}