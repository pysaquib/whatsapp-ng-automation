module.exports = function main() {
    const puppeteer = require('puppeteer');
    (async () => {
        const browser = await puppeteer.launch({ headless: false, userDataDir: "./puppeteer_data", defaultViewport: null, args: ['--start-maximized'] });
        let phoneNum = '918180025497';
        let message = "Hi%20hELLO.%20Ignore%20this%20message%20I'm%20testing%20automation";
    
        let selector = '#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button';
        const page = await browser.newPage();
        await page.goto(`https://web.whatsapp.com/send?phone=+${phoneNum}&text=${message}`); 
        
        //Wait for the send button to be loaded
        await page.waitForSelector(selector);
        
        // Click on Send button
        await page.click(selector);
        browser.close();
    })();
}

