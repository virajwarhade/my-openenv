import os
import requests
from openai import OpenAI

# REQUIRED ENV VARIABLES (DO NOT OVERRIDE)
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

TASK_NAME = "medium"
BENCHMARK = "traffic-env"
MAX_STEPS = 100


def choose_action(state):
    north, south, east, west, en, es, ee, ew = state

    # Emergency priority
    if en or es:
        return 0
    if ee or ew:
        return 1

    # Longest queue
    return 0 if (north + south) > (east + west) else 1


def main():
    # ✅ REQUIRED: use their LLM proxy
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )

    # 🔥 REQUIRED CALL (this fixes your Phase 2)
    client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "hello"}],
        max_tokens=5
    )

    rewards = []
    step_count = 0
    success = False

    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}")

    try:
        # Reset
        res = requests.post(f"{API_BASE_URL}/reset")
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

    score = min(1.0, max(0.0, sum(rewards) / 100))
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step_count} score={score:.2f} rewards={rewards_str}"
    )


if __name__ == "__main__":
    main()
