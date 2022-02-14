from gym.envs.registration import register

register(
    id='Ataxx-v0',
    entry_point='ataxx.envs.ataxx:AtaxxEnv',
)
