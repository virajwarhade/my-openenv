import random
import numpy as np

class TrafficEnv:
    def __init__(self, config=None):
        self.config = config or {
            "spawn_rate": 2,
            "emergency_prob": 0.05,
            "max_steps": 100
        }
        self.max_cars = 20
        self.reset()

    def reset(self):
        self.north = random.randint(0, 5)
        self.south = random.randint(0, 5)
        self.east = random.randint(0, 5)
        self.west = random.randint(0, 5)

        self.emergency_lane = None
        self.time = 0

        # Metrics
        self.total_wait = 0
        self.total_passed = 0
        self.emergency_delay = 0

        return self._get_state()

    def _get_state(self):
        return np.array([
            self.north,
            self.south,
            self.east,
            self.west,
            int(self.emergency_lane == "north"),
            int(self.emergency_lane == "south"),
            int(self.emergency_lane == "east"),
            int(self.emergency_lane == "west"),
        ], dtype=np.float32)

    def step(self, action):
        reward = 0

        # Spawn cars
        self._spawn_cars()

        # Emergency spawn
        if random.random() < self.config["emergency_prob"]:
            self.emergency_lane = random.choice(["north", "south", "east", "west"])

        passed = 0

        if action == 0:  # NS green
            passed = min(self.north, 2) + min(self.south, 2)
            self.north = max(0, self.north - 2)
            self.south = max(0, self.south - 2)

            waiting = self.east + self.west

            if self.emergency_lane in ["north", "south"]:
                reward += 15
                self.emergency_lane = None
            elif self.emergency_lane in ["east", "west"]:
                self.emergency_delay += 1
                reward -= 5

        elif action == 1:  # EW green
            passed = min(self.east, 2) + min(self.west, 2)
            self.east = max(0, self.east - 2)
            self.west = max(0, self.west - 2)

            waiting = self.north + self.south

            if self.emergency_lane in ["east", "west"]:
                reward += 15
                self.emergency_lane = None
            elif self.emergency_lane in ["north", "south"]:
                self.emergency_delay += 1
                reward -= 5

        # Reward logic
        reward += passed * 2
        reward -= waiting

        # Metrics
        self.total_wait += waiting
        self.total_passed += passed

        self.time += 1
        done = self.time >= self.config["max_steps"]

        return self._get_state(), reward, done, {}

    def _spawn_cars(self):
        self.north = min(self.max_cars, self.north + random.randint(0, self.config["spawn_rate"]))
        self.south = min(self.max_cars, self.south + random.randint(0, self.config["spawn_rate"]))
        self.east = min(self.max_cars, self.east + random.randint(0, self.config["spawn_rate"]))
        self.west = min(self.max_cars, self.west + random.randint(0, self.config["spawn_rate"]))