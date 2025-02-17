import numpy as np
import gymnasium as gym
from bee import BeeWorld
import torch.nn as nn

from stable_baselines3 import TD3
from stable_baselines3.common.noise import (
    NormalActionNoise,
    OrnsteinUhlenbeckActionNoise,
)


gym.register(
    id="BeeWorld",
    entry_point=BeeWorld,
    max_episode_steps=1000,
)

env = gym.make("BeeWorld", render_mode="human", max_episode_steps=1000)
env.reset()

# The noise objects for TD3
# action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=0.1) # alternative noise TBD
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(
    mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions)
)


policy_kwargs = {
    "net_arch": [100, 100],  # Specify the number of hidden units per layer
    "activation_fn": nn.ReLU,  # Specify the activation function
}

model = TD3(
    "MultiInputPolicy",
    env,
    action_noise=action_noise,
    verbose=1,
    policy_kwargs=policy_kwargs,
    # learning_rate=3e-4,
    tensorboard_log="./logs/",
)
model.learn(total_timesteps=1_000_000, log_interval=10)

vec_env = model.get_env()
obs = vec_env.reset()

while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = vec_env.step(action)

env.close()
model.save("test2")
