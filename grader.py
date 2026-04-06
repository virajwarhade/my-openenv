def compute_score(env):
    avg_wait = env.total_wait / max(1, env.time)
    throughput = env.total_passed / max(1, env.time)
    emergency_penalty = env.emergency_delay

    wait_score = max(0, 1 - avg_wait / 20)
    throughput_score = min(1, throughput / 5)
    emergency_score = max(0, 1 - emergency_penalty / 10)

    final_score = (
        0.4 * wait_score +
        0.4 * throughput_score +
        0.2 * emergency_score
    )

    return round(final_score, 2)