# tools

One `<tool>.yaml` file per voice platform. Keeping each tool in its own file makes it easy to compare setups and open pull requests without merge conflicts.

Each file lists the tool's board name, how to pin the agent and number to call (an id in the file or in `.env`; none is committed), the greeting and prompt the agent must use, and the values its setup script in `harness/provision/` needs.

Every tool runs on its out-of-the-box defaults: `model`, `stt` and `tts` stay `null`, and the bench records whatever the platform picked. The defaults are the product being measured.

Prices are not listed here on purpose. Each call is priced from the platform's own billing record, never from a rate card.

To add or update a tool: edit `tools/<tool>.yaml`, run `.venv/bin/pytest`, and open a pull request.
