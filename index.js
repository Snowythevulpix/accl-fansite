import { parse } from 'node-html-parser';
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

app.get("/characters/:id", async (req, res) => {
    const id = req.params.id
    const dataRaw = (await readFile(__dirname + "/data/characters.json")).toString()
    const data = JSON.parse(dataRaw)
    const finalData = data[id - 1];
    const root = parse((await readFile(__dirname + "/tmpl/character.html")).toString())
    const container = root.querySelector("#profile-container")
    console.log(finalData)
    for (const key in finalData){
        if (key !== "id"){
            container.appendChild(parse(`<p>${key}: ${finalData[key]}</p>`))
        }
    }
    res.send(root.toString())
})

app.get("/anime", (req, res) => {
    res.sendFile(join(__dirname, "/routes/anime.html"))
})

app.get("/staff", (req, res) => {
    res.sendFile(join(__dirname, "/routes/staff.html"))
})

app.get("/music", (req, res) => {
    res.sendFile(join(__dirname, "/routes/music.html"))
})

app.get("/api/characters", async (req, res) => {
    const dataRaw = (await readFile(__dirname + "/data/characters.json")).toString()
    const data = JSON.parse(dataRaw)
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
})

app.get("/api/anime", async (req, res) => {
    const dataRaw = (await readFile(__dirname + "/data/anime.json")).toString()
    const data = JSON.parse(dataRaw)
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
})

app.get("/api/staff", async (req, res) => {
    const dataRaw = (await readFile(__dirname + "/data/staff.json")).toString()
    const data = JSON.parse(dataRaw)
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
})

app.get("/api/music", async (req, res) => {
    const dataRaw = (await readFile(__dirname + "/data/music.json")).toString()
    const data = JSON.parse(dataRaw)
    res.setHeader('Content-Type', 'application/json');
    res.send(data);
})

app.listen(PORT, (err) => {
    if (err) console.error(err);
    console.log("Server listening on port " + PORT)
})