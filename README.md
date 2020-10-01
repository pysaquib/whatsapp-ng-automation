# whatsapp-ng-automation

## Install Dependencies
`pip3 install -r requirements.txt`

`pip3 install requests` to update the urllib version

## Install geckodriver for Firefox
https://github.com/mozilla/geckodriver/releases

Set the executable path: `PATH=$PATH:/path-to-geckodriver`


## Run
`python3 send_message.py`

When prompted to login, there would be a login_**.png created in the current directory, scan the QR code with your phone, then press ENTER in the terminal prompt.

##Config
Check `HEADLESS`, `DEFAULT_WAIT_TIMEOUT`, `CONTACTS_URL` in the constants section of the script to change these configs.
