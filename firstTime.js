//This function is required for first time login for session creation.
//Session is saved in ./puppeteer_data folder
/*
    If user logs out from whatsapp from phone or login is required in any scenario,
    make sure to delete ./puppeteer_data folder
*/

const puppeteer = require('puppeteer');
(async () => {
    //userDataDir key saves the session for first time login
    const browser = await puppeteer.launch({ headless: false, userDataDir: "./puppeteer_data", defaultViewport: null, args: ['--start-maximized'] });
    let phoneNum = '918981174121';
    let message = "Hi%20hELLO.%20Ignore%20this%20message%20I'm%20testing%20automation";

    let selector = '#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button';
    const page = await browser.newPage();
    await page.goto(`https://web.whatsapp.com/send?phone=+${phoneNum}&text=${message}`); 
    await page.waitForSelector(selector);
    browser.close();
})();

