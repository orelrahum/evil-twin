const express = require('express')
const app = express()
const port = 80

const html = `<div> <h1><form method="post" path="/password"></form> FUCK YOU </h1> </div>`

app.get('/', (req, res) => {
    console.log('adasdasdasd')
    res.send(html);
});

app.post('/password', (req, res) => {
    console.log('req.body', req.body);
    res.send("you've' benn hacked");
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})
