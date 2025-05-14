import express from "express";
import { join } from "path"
import { readFile } from "fs/promises";


const app = express();
const PORT = 3000;
const __dirname = import.meta.dirname;

app.use(express.static(__dirname + '/public'));
console.log(__dirname + "/public")
app.get("/", (req, res) => {
    res.sendFile(join(__dirname, "/index.html"))
})

app.get("/characters", (req, res) => {
    res.sendFile(join(__dirname, "/routes/characters.html"))
})

app.get("/api/characters", async (req, res) => {
    const dataRaw = (await readFile(__dirname + "/data/characters.json")).toString()
    const data = JSON.parse(dataRaw)
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
})

app.listen(PORT, (err) => {
    if (err) console.error(err);
    console.log("Server listening on port " + PORT)
})