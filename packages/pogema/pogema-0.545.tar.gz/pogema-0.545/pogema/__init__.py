from gym import register
from pogema.grid_config import GridConfig

__version__ = '0.545'

__all__ = [
    'GridConfig',
]

register(
    id="Pogema-v0",
    entry_point="pogema.envs:Pogema",
)

register(
    id='PogemaCoopFinish-v0',
    entry_point="pogema.envs:PogemaCoopFinish"
)
