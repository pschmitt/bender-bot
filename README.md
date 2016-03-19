# bender-bot

This is a telegram bot that does stuff.

## Installation

```bash
git clone --recursive https://github.com/pschmitt/bender-bot
cd bender-bot
pip install -r requirement.txt
cp bender-bot.service ~/.config/systemd/user
```

## Configuration

Edit the [bender.yaml.sample](bender.yaml.sample) file and move it:

```bash
mv bender.yaml.sample bender.yaml
```

## Start

```bash
systemctl --user start bender-bot.service
```

## License

[GPL3](LICENSE)
