const express = require("express");
const bodyParser = require("body-parser");
const data = require("./data");
const MedBazaar = require("./models/medicine");
const app = express();

app.use(express.static('public'))

app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");

//SAVE DATA IN DATABASE

// data.forEach(function(medicine){
//     const med = new MedBazaar({
//         name: medicine.pname,
//          size: medicine.psize,
//         price: medicine.mrp,
//         company: medicine.pcompany,

//     });
//     med.save(function(err){
//         if(!err){
//             console.log("Data saved");
//         }
//     });
// })
let options = [];


app.get("/", (req, res) => {
  //GET DATA FROM DATABASE
  MedBazaar.find({}, function (err, medicines) {
    if (err) {
      console.log(err);
    } else {
      medicines.forEach(function (med) {
        options.push(med.name);
      });
    }
    // console.log(options);
    res.render("index", {params: options})
  });


  //Handle search request
  app.post("/search", (req, res) => {
    

    // res.send("Search successful");
    console.log(req.body);
    MedBazaar.find({name:req.body.input},function(err, medicines){
        if(err){
            console.log(err);
        } else{
            console.log(medicines);
            res.render("medicine", {name: req.body.input,
                params: medicines})
        }
    })
  });
});

app.listen(8000, () => {
  console.log("Server is listening to port 8000");
});
