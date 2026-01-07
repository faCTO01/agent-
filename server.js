import express from "express";
import { spawn } from "child_process";

const app = express();
app.use(express.json());

// Ендпоінт для відправки тексту в ядро Spark
app.post("/say", (req, res) => {
  const text = req.body.text || "";
  const py = spawn("python3", ["core/run_once.py", text], { stdio: "inherit" });

  py.on("close", (code) => {
    res.json({ status: code === 0 ? "ok" : "error" });
  });
});

app.listen(3000, () => console.log("Spark-1 terminal ready on :3000"));
