module.exports = async function getContacts() {
    
    const axios = require('axios');
    let contacts = {}

    await axios.get('https://sheetdb.io/api/v1/ybynjbo13n0bk')
        .then((res) => {
            // console.log(res.data);
            contacts = res.data;
        })
        .catch(err => {
            console.log(err)
        });
    return contacts;
}