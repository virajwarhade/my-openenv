import os
import requests
import random
from openai import OpenAI

# ENV VARIABLES (required)
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

TASK_NAME = os.getenv("TASK", "medium")
BENCHMARK = "traffic-env"
MAX_STEPS = 100

# OpenAI client (required by rules)
client = OpenAI(
    base_url=os.getenv("API_BASE_URL_LLM", "https://router.huggingface.co/v1"),
    api_key=HF_TOKEN
)


def choose_action(state):
    """
    Smart baseline agent:
    - Prioritize emergency
    - Otherwise longest queue
    """

    north, south, east, west, en, es, ee, ew = state

    # Emergency priority
    if en or es:
        return 0  # NS green
    if ee or ew:
        return 1  # EW green

    # Longest queue logic
    if (north + south) > (east + west):
        return 0
    else:
        return 1


def main():
    rewards = []
    step_count = 0
    success = False

    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

    try:
        # Reset environment
        res = requests.post(f"{API_BASE_URL}/reset", json={"task": TASK_NAME})
        state = res.json()["state"]

        done = False

        while not done and step_count < MAX_STEPS:
            step_count += 1

            action = choose_action(state)

            res = requests.post(
                f"{API_BASE_URL}/step",
                json={"action": action}
            )

            data = res.json()

            state = data["state"]
            reward = float(data["reward"])
            done = data["done"]

            rewards.append(reward)

            print(
                f"[STEP] step={step_count} action={action} "
                f"reward={reward:.2f} done={str(done).lower()} error=null"
            )

        success = True

    except Exception as e:
        print(
            f"[STEP] step={step_count} action=null "
            f"reward=0.00 done=true error={str(e)}"
        )

    # Final score (simple normalization)
    score = min(1.0, max(0.0, sum(rewards) / 100))

    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step_count} score={score:.2f} rewards={rewards_str}"
    )


if __name__ == "__main__":
    main()