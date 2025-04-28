// server.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const { exec } = require("child_process");
const fs = require("fs");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post("/run", (req, res) => {
  const { language, code } = req.body;

  let filename;
  let command;

  switch (language) {
    case "python":
      filename = "code.py";
      fs.writeFileSync(filename, code);
      command = `python3 ${filename}`;
      break;
    case "cpp":
      filename = "code.cpp";
      fs.writeFileSync(filename, code);
      command = `g++ ${filename} -o code && ./code`;
      break;
    case "c":
      filename = "code.c";
      fs.writeFileSync(filename, code);
      command = `gcc ${filename} -o code && ./code`;
      break;
    case "java":
      filename = "Main.java";
      fs.writeFileSync(filename, code);
      command = `javac Main.java && java Main`;
      break;
    case "csharp":
      filename = "Program.cs";
      fs.writeFileSync(filename, code);
      command = `mcs ${filename} && mono Program.exe`;
      break;
    case "javascript":
      filename = "code.js";
      fs.writeFileSync(filename, code);
      command = `node ${filename}`;
      break;
    default:
      return res.status(400).send({ output: "Unsupported Language" });
  }

  exec(command, (error, stdout, stderr) => {
    if (error) {
      res.send({ output: stderr || error.message });
    } else {
      res.send({ output: stdout });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
