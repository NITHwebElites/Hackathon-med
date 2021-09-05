const mongoose = require("mongoose");
require("dotenv").config();

mongoose.connect(process.env.DATABASE, {useNewUrlParser: true, useUnifiedTopology: true});
console.log("Mongoose connection open");
const medSchema = new mongoose.Schema({
  name: String,
  price: String,
  company: String,
  
});
module.exports = mongoose.model("MedBazaar", medSchema);
