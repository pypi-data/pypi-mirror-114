# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcadezero', 'arcadezero.examples']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.5.7,<3.0.0']

setup_kwargs = {
    'name': 'arcadezero',
    'version': '0.0.1',
    'description': 'A beginner friendly layer on top of Arcade to create your very first game',
    'long_description': '# arcadezero\nA beginner friendly layer on top of Arcade to create your very first game.\n\n> Hint for arcade devs: ArcadeZero uses a wrapper of `arcade.Sprite` to reduce \n> the available methods and provide a easier start into game development.\n> The main focus is to code your first game.\n\n## Your first game\n![Screenshot](docs/coin_paradise.png)\n\n\n\n## Basic commands\n\n\n```python\nfrom arcadezero import *\n\n\n# ...\n```\n\n\n## ZeroSprites\n\nA sprite is a figure, which has a position and an image.\nArcadeZero come with a few default ones.\n\nTo start with the game, it is enough to create them. they will be drawn automatically.\n\n```python\ncoin = Coin()\nsilvercoin = SilverCoin()\nplayermale = PlayerMale()\nplayerfemale = PlayerFemale()\nbee = Bee()\nsaw = Saw()\n```\n\n### Functions\n\n- `sprite.move(dx=0, dy=0)` - moves the Sprite into a direction\n- `sprite.move_left(dx=0)` - moves the Sprite left\n- `sprite.move_right(dx=0)` - moves the Sprite right\n- `sprite.move_up(dy=0)` - moves the Sprite up\n- `sprite.move_down(dy=0)` - moves the Sprite down\n- `sprite.rotate(angle)` - rotates the Sprite\n\n## Example from Screenshot\n\nMove the player with the arrow keys, you can add more Coins by pressing `SPACE`.\nDo not touch the saws!\n\n```python\nfrom arcadezero import *\nfrom arcadezero import sounds\n\nscore = Score("Your score is: ", 0)\n\nplayer = PlayerMale(200, 200)\n\n\n@player.when_key(keys.SPACE)\ndef new_coin_on_space(player, key):\n    Coin().with_rand_pos()\n\n\n@player.while_key(keys.UP, keys.DOWN)\ndef player_move(player, key):\n    if key == keys.UP:\n        player.move_up(10)\n\n    if key == keys.DOWN:\n        player.move_down(10)\n\n\n@player.while_key(keys.LEFT)\ndef player_move(player, key):\n    player.move_left(10)\n\n\n@player.while_key(keys.RIGHT)\ndef player_move(player, key):\n    player.move_right(10)\n\n\n@player.when_collide_with(Coin)\ndef player_move(player, coin):\n    coin.remove()\n    score + 20\n    sounds.coin1.play()\n\n    if len(Coin.all()) == 0:\n        player.remove()\n        show_message(f"You won with {score} points.")\n\n\n@player.when_collide_with(Saw)\ndef player_move(player, saw):\n    player.remove()\n    show_message("You lost", color=colors.COAL)\n\n\n@when_start\ndef setup():\n    set_background_color(colors.CORN)\n\n    # Lege 2 neue Coins an\n    Coin().with_rand_pos()\n    Coin().with_rand_pos()\n\n    # Und 2 Gegner\n    Saw().with_rand_pos()\n    Saw().with_rand_pos()\n\n\nrun(1200, 800)\n```\n',
    'author': 'Maic Siemering',
    'author_email': 'maic@siemering.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eruvanos/arcadezero',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
