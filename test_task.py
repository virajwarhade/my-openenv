from env import TrafficEnv
from tasks import get_task_config
from grader import compute_score
import random

task = "hard"
config = get_task_config(task)

env = TrafficEnv(config=config)
state = env.reset()

done = False

while not done:
    action = random.randint(0, 1)
    state, reward, done, _ = env.step(action)

score = compute_score(env)

print("Task:", task)
print("Score:", score)