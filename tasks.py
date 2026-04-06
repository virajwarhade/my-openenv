def get_task_config(task_name):
    if task_name == "easy":
        return {
            "spawn_rate": 1,
            "emergency_prob": 0.01,
            "max_steps": 50
        }

    elif task_name == "medium":
        return {
            "spawn_rate": 2,
            "emergency_prob": 0.05,
            "max_steps": 100
        }

    elif task_name == "hard":
        return {
            "spawn_rate": 3,
            "emergency_prob": 0.1,
            "max_steps": 150
        }

    else:
        raise ValueError("Invalid task name")