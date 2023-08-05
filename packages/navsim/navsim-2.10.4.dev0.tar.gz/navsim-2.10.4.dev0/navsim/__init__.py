import os

# Path(__file__).parent.joinpath('version.txt')
with open(os.path.join(os.path.dirname(__file__), 'version.txt'), 'r') as vf:
    __version__ = vf.read().strip()



from navsim import util, agent, executor, env


__all__ = ['agent', 'util', 'executor','env']
