const express = require('express');
const app = express();
const port = process.env.PORT||2000;
app.use(express.static("public"))
app.set("view engine","ejs");
 app.get("/",(req,res)=>{
   
    res.render("index");
 })
 app.listen(port,()=>{
     console.log("server is running !!");
 })
 //rgba(153, 164, 206, 0.719),rgba(16, 79, 109, 0.479)rgba(153, 164, 206, 0.719),rgba(16, 79, 109, 0.479)