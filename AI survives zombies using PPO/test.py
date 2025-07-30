import os
import re
from stable_baselines3 import PPO
from environment import ZombieEnvironment

MODELS_DIR = "test"
EPISODES_PER_MODEL = 5

# Sort function to handle numerical order in filenames like "timmy_ppo_model_10000"


def extract_timesteps(name):
    match = re.search(r"(\d+)", name)
    return int(match.group(1)) if match else -1


def run_model(model_path, env, num_episodes):
    print(f"\nRunning model: {model_path}")
    model = PPO.load(model_path)
    for episode in range(num_episodes):
        obs = env.reset()
        done = False
        total_reward = 0
        while not done:
            action, _states = model.predict(obs)
            obs, reward, done, info = env.step(action)
            env.render()
            total_reward += reward
        print(f"Episode {episode + 1}: Total Reward = {total_reward:.2f}")


def main():
    env = ZombieEnvironment()

    model_files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".zip")]
    model_files.sort(key=extract_timesteps)  # Sort by training step

    for model_file in model_files:
        model_path = os.path.join(MODELS_DIR, model_file)
        run_model(model_path, env, EPISODES_PER_MODEL)

    env.close()


if __name__ == "__main__":
    main()
