module.exports = async function main(C) {
    const puppeteer = require('puppeteer');

    let selector = '#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button';

    const browser = await puppeteer.launch({ headless: false, userDataDir: "./puppeteer_data", defaultViewport: null, args: ['--start-maximized'] });

    async function sender(phoneNum) {
        const message = `Hi, How are you doing>?`
        const page = await browser.newPage();
        await page.goto(`https://web.whatsapp.com/send?phone=+${phoneNum}&text=${message}`);         
        await page.waitForSelector(selector);
        
        await page.click(selector);
        setTimeout(() => {
            page.close();
        }, 4000)
    }



    let i = 0;
    (function timerCall(i) {
        const m = 
        setTimeout( () => {
            console.log(C[i])
            sender('91'.concat(C[i]['Number']))
            if(i <= C.length - 1) {
                timerCall(i+1)
            }
            else{
                browser.close()
            }
        }, 20000)
    })(i)
}
