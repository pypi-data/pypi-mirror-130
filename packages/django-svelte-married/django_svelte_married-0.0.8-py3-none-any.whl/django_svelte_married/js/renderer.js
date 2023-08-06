const {performance} = require('perf_hooks');
const express = require("express");
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());
app.post('/', function (req, res) {
    const exported = require('./../out/ssr');
    const renderStart = performance.now();
    if (!exported[req.body.component]) {
        console.error(`Component ${req.body.component} is not in exported.js.`);
        res.send(JSON.stringify({html: ''}));
        return;
    }
    const rendered = exported[req.body.component].render(JSON.parse(req.body.props) || {});
    console.info(`Rendered component ${req.body.component} with props '${req.body.props}' in ${Math.round(performance.now() - renderStart)}ms`);
    res.send(JSON.stringify({html: rendered.html}));
});
const appPort = process.env.SVELTE_SSR_PORT ? parseInt(process.env.SVELTE_SSR_PORT) : 6060;
app.listen(appPort, () => console.log(`The server started at localhost:${appPort}`));
