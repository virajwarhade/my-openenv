from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import sys
import os
from models import Action, ResetRequest
from fastapi.responses import HTMLResponse

# Fix imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from env import TrafficEnv
from tasks import get_task_config

app = FastAPI()
env = TrafficEnv()



class ResetRequest(BaseModel):
    task: str = "medium"


class Action(BaseModel):
    action: int

@app.get("/web", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Traffic Control UI</title>
        <style>
            body {
                font-family: Arial;
                margin: 0;
                display: flex;
                height: 100vh;
            }

            .left, .right {
                width: 50%;
                padding: 20px;
                box-sizing: border-box;
            }

            .left {
                background: #f5f5f5;
            }

            .right {
                background: #ffffff;
                border-left: 2px solid #ddd;
            }

            h2 {
                margin-top: 0;
            }

            button {
                padding: 10px 20px;
                margin: 5px;
                cursor: pointer;
            }

            .box {
                background: #fff;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }

            #history {
                max-height: 300px;
                overflow-y: auto;
                font-size: 14px;
            }

            pre {
                margin: 0;
            }
        </style>
    </head>

    <body>

        <!-- LEFT PANEL -->
        <div class="left">
            <h2>🚦 Take Action</h2>

            <button onclick="resetEnv()">Reset Environment</button><br>
            <button onclick="stepEnv(0)">NS Green</button>
            <button onclick="stepEnv(1)">EW Green</button>

            <div class="box">
                <h3>Current State</h3>
                <pre id="state">Click Reset</pre>
            </div>

            <div class="box">
                <h3>Status</h3>
                <div id="status">Idle</div>
            </div>
        </div>

        <!-- RIGHT PANEL -->
        <div class="right">
            <h2>📊 State Observer</h2>

            <div class="box">
                <h3>Observation</h3>
                <pre id="observation">{}</pre>
            </div>

            <div class="box">
                <h3>Action History</h3>
                <div id="history"></div>
            </div>
        </div>

        <script>
            let stepCount = 0;

            async function resetEnv() {
                let res = await fetch('/reset', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({task: "medium"})
                });

                let data = await res.json();

                document.getElementById('state').innerText = JSON.stringify(data.state, null, 2);
                document.getElementById('observation').innerText = JSON.stringify(data, null, 2);
                document.getElementById('history').innerHTML = "";
                document.getElementById('status').innerText = "Environment Reset";
                stepCount = 0;
            }

            async function stepEnv(action) {
                let res = await fetch('/step', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({action: action})
                });

                let data = await res.json();

                stepCount++;

                document.getElementById('state').innerText = JSON.stringify(data.state, null, 2);
                document.getElementById('observation').innerText = JSON.stringify(data, null, 2);

                let history = document.getElementById('history');
                let entry = document.createElement('div');

                entry.innerHTML = `
                    <b>Step ${stepCount}</b><br>
                    Action: ${action}<br>
                    Reward: ${data.reward}<br>
                    Done: ${data.done}<br>
                    <hr>
                `;

                history.prepend(entry);

                document.getElementById('status').innerText = data.done ? "Episode Finished" : "Running";
            }
        </script>

    </body>
    </html>
    """

@app.post("/reset")
def reset(req: ResetRequest):
    global env
    config = get_task_config(req.task)
    env = TrafficEnv(config=config)
    state = env.reset()
    return {"state": state.tolist()}


@app.post("/step")
def step(action: Action):
    state, reward, done, _ = env.step(action.action)
    return {
        "state": state.tolist(),
        "reward": float(reward),
        "done": done
    }


@app.get("/state")
def get_state():
    return {"state": env._get_state().tolist()}



# ✅ REQUIRED MAIN FUNCTION
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()