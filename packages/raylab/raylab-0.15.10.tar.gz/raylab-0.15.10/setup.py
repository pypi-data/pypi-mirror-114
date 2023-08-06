# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raylab',
 'raylab.agents',
 'raylab.agents.acktr',
 'raylab.agents.mage',
 'raylab.agents.mbpo',
 'raylab.agents.naf',
 'raylab.agents.sac',
 'raylab.agents.sop',
 'raylab.agents.svg',
 'raylab.agents.svg.inf',
 'raylab.agents.svg.one',
 'raylab.agents.svg.soft',
 'raylab.agents.td3',
 'raylab.agents.trpo',
 'raylab.cli',
 'raylab.envs',
 'raylab.envs.environments',
 'raylab.envs.environments.lqr',
 'raylab.envs.wrappers',
 'raylab.execution',
 'raylab.logger',
 'raylab.policy',
 'raylab.policy.losses',
 'raylab.policy.model_based',
 'raylab.policy.modules',
 'raylab.policy.modules.actor',
 'raylab.policy.modules.actor.policy',
 'raylab.policy.modules.critic',
 'raylab.policy.modules.model',
 'raylab.policy.modules.model.stochastic',
 'raylab.policy.modules.networks',
 'raylab.torch',
 'raylab.torch.distributions',
 'raylab.torch.nn',
 'raylab.torch.nn.distributions',
 'raylab.torch.nn.distributions.flows',
 'raylab.torch.nn.modules',
 'raylab.torch.optim',
 'raylab.tune',
 'raylab.utils',
 'raylab.utils.exploration']

package_data = \
{'': ['*']}

install_requires = \
['bokeh<2.3.3',
 'click>=7.1.2,<8.0.0',
 'dataclasses-json>=0.5.1,<0.6.0',
 'dm-tree>=0.1.5,<0.2.0',
 'opencv-contrib-python>=4.4.0,<5.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'poetry-version>=0.1.5,<0.2.0',
 'pytorch-lightning>=1.3.8,<1.4.0',
 'ray[tune,rllib]<1.5',
 'sklearn>=0.0,<0.1',
 'streamlit>=0.62,<0.83',
 'tabulate>=0.8.7,<0.9.0',
 'torch>=1.5.1,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "4.0"': ['cachetools>=4.1.0,<5.0.0']}

entry_points = \
{'console_scripts': ['raylab = raylab.cli:raylab']}

setup_kwargs = {
    'name': 'raylab',
    'version': '0.15.10',
    'description': 'Reinforcement learning algorithms in RLlib and PyTorch.',
    'long_description': '======\nraylab\n======\n\n|PyPI| |Tests| |Dependabot| |License| |CodeStyle|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/raylab?logo=PyPi&logoColor=white&color=blue\n      :alt: PyPI\n\n.. |Tests| image:: https://img.shields.io/github/workflow/status/angelolovatto/raylab/Poetry%20package?label=tests&logo=GitHub\n       :alt: GitHub Workflow Status\n\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=angelolovatto/raylab\n        :target: https://dependabot.com\n\n.. |License| image:: https://img.shields.io/github/license/angelolovatto/raylab?color=blueviolet&logo=github\n         :alt: GitHub\n\n.. |CodeStyle| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n           :target: https://github.com/psf/black\n\n\nReinforcement learning algorithms in `RLlib <https://github.com/ray-project/ray/tree/master/rllib>`_\nand `PyTorch <https://pytorch.org>`_.\n\n\nInstallation\n------------\n\n.. code:: bash\n\n          pip install raylab\n\n\nQuickstart\n----------\n\nRaylab provides agents and environments to be used with a normal RLlib/Tune setup.\nYou can an agent\'s name (from the `Algorithms`_ section) to :code:`raylab info list` to list its top-level configurations:\n\n.. code-block:: zsh\n\n    raylab info list SoftAC\n\n.. code-block::\n\n    learning_starts: 0\n        Hold this number of timesteps before first training operation.\n    policy: {}\n        Sub-configurations for the policy class.\n    wandb: {}\n        Configs for integration with Weights & Biases.\n\n        Accepts arbitrary keyword arguments to pass to `wandb.init`.\n        The defaults for `wandb.init` are:\n        * name: `_name` property of the trainer.\n        * config: full `config` attribute of the trainer\n        * config_exclude_keys: `wandb` and `callbacks` configs\n        * reinit: True\n\n        Don\'t forget to:\n          * install `wandb` via pip\n          * login to W&B with the appropriate API key for your\n            team/project.\n          * set the `wandb/project` name in the config dict\n\n        Check out the Quickstart for more information:\n        `https://docs.wandb.com/quickstart`\n\nYou can add the :code:`--rllib` flag to get the descriptions for all the options common to RLlib agents\n(or :code:`Trainer`\\s)\n\nLaunching experiments can be done via the command line using :code:`raylab experiment` passing a file path\nwith an agent\'s configuration through the :code:`--config` flag.\nThe following command uses the cartpole `example <examples/PG/cartpole_defaults.py>`_ configuration file\nto launch an experiment using the vanilla Policy Gradient agent from the RLlib library.\n\n.. code-block:: zsh\n\n    raylab experiment PG --name PG -s training_iteration 10 --config examples/PG/cartpole_defaults.py\n\nYou can also launch an experiment from a Python script normally using Ray and Tune.\nThe following shows how you may use Raylab to perform an experiment comparing different\ntypes of exploration for the NAF agent.\n\n.. code-block:: python\n\n             import ray\n             from ray import tune\n             import raylab\n\n             def main():\n                 raylab.register_all_agents()\n                 raylab.register_all_environments()\n                 ray.init()\n                 tune.run(\n                     "NAF",\n                     local_dir="data/NAF",\n                     stop={"timesteps_total": 100000},\n                     config={\n                         "env": "CartPoleSwingUp-v0",\n                         "exploration_config": {\n                             "type": tune.grid_search([\n                                 "raylab.utils.exploration.GaussianNoise",\n                                 "raylab.utils.exploration.ParameterNoise"\n                             ])\n                         }\n                     },\n                     num_samples=10,\n                 )\n\n             if __name__ == "__main__":\n                 main()\n\n\nOne can then visualize the results using :code:`raylab dashboard`, passing the :code:`local_dir` used in the\nexperiment. The dashboard lets you filter and group results in a quick way.\n\n.. code-block:: zsh\n\n    raylab dashboard data/NAF/\n\n\n.. image:: https://i.imgur.com/bVc6WC5.png\n        :align: center\n\n\nYou can find the best checkpoint according to a metric (:code:`episode_reward_mean` by default)\nusing :code:`raylab find-best`.\n\n.. code-block:: zsh\n\n    raylab find-best data/NAF/\n\nFinally, you can pass a checkpoint to :code:`raylab rollout` to see the returns collected by the agent and\nrender it if the environment supports a visual :code:`render()` method. For example, you\ncan use the output of the :code:`find-best` command to see the best agent in action.\n\n\n.. code-block:: zsh\n\n    raylab rollout $(raylab find-best data/NAF/) --agent NAF\n\n\nAlgorithms\n----------\n\n+--------------------------------------------------------+-------------------------+\n| Paper                                                  | Agent Name              |\n+--------------------------------------------------------+-------------------------+\n| `Actor Critic using Kronecker-factored Trust Region`_  | ACKTR                   |\n+--------------------------------------------------------+-------------------------+\n| `Trust Region Policy Optimization`_                    | TRPO                    |\n+--------------------------------------------------------+-------------------------+\n| `Normalized Advantage Function`_                       | NAF                     |\n+--------------------------------------------------------+-------------------------+\n| `Stochastic Value Gradients`_                          | SVG(inf)/SVG(1)/SoftSVG |\n+--------------------------------------------------------+-------------------------+\n| `Soft Actor-Critic`_                                   | SoftAC                  |\n+--------------------------------------------------------+-------------------------+\n| `Streamlined Off-Policy`_ (DDPG)                       | SOP                     |\n+--------------------------------------------------------+-------------------------+\n| `Model-Based Policy Optimization`_                     | MBPO                    |\n+--------------------------------------------------------+-------------------------+\n| `Model-based Action-Gradient-Estimator`_               | MAGE                    |\n+--------------------------------------------------------+-------------------------+\n\n\n.. _`Actor Critic using Kronecker-factored Trust Region`: https://arxiv.org/abs/1708.05144\n.. _`Trust Region Policy Optimization`: http://proceedings.mlr.press/v37/schulman15.html\n.. _`Normalized Advantage Function`: http://proceedings.mlr.press/v48/gu16.html\n.. _`Stochastic Value Gradients`: http://papers.nips.cc/paper/5796-learning-continuous-control-policies-by-stochastic-value-gradients\n.. _`Soft Actor-Critic`: http://proceedings.mlr.press/v80/haarnoja18b.html\n.. _`Model-Based Policy Optimization`: http://arxiv.org/abs/1906.08253\n.. _`Streamlined Off-Policy`: https://arxiv.org/abs/1910.02208\n.. _`Model-based Action-Gradient-Estimator`: https://arxiv.org/abs/2004.14309\n\n\nCommand-line interface\n----------------------\n\n.. role:: bash(code)\n   :language: bash\n\nFor a high-level description of the available utilities, run :bash:`raylab --help`\n\n.. code:: bash\n\n    Usage: raylab [OPTIONS] COMMAND [ARGS]...\n\n      RayLab: Reinforcement learning algorithms in RLlib.\n\n    Options:\n      --help  Show this message and exit.\n\n    Commands:\n      dashboard    Launch the experiment dashboard to monitor training progress.\n      episodes     Launch the episode dashboard to monitor state and action...\n      experiment   Launch a Tune experiment from a config file.\n      find-best    Find the best experiment checkpoint as measured by a metric.\n      info         View information about an agent\'s config parameters.\n      rollout      Wrap `rllib rollout` with customized options.\n      test-module  Launch dashboard to test generative models from a checkpoint.\n\n\nPackages\n--------\n\nThe project is structured as follows\n::\n\n    raylab\n    |-- agents            # Trainer and Policy classes\n    |-- cli               # Command line utilities\n    |-- envs              # Gym environment registry and utilities\n    |-- logger            # Tune loggers\n    |-- policy            # Extensions and customizations of RLlib\'s policy API\n    |   |-- losses        # RL loss functions\n    |   |-- modules       # PyTorch neural network modules for TorchPolicy\n    |-- pytorch           # PyTorch extensions\n    |-- utils             # miscellaneous utilities\n',
    'author': 'Ângelo Gregório Lovatto',
    'author_email': 'angelolovatto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/angelolovatto/raylab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
