# nodeb

## Installation

1. Install Python 3.10 or newer on each machine.
2. Clone this repository to every machine that will participate in the
   cluster:

   ```bash
   git clone <repo-url>
   cd nodeb
   ```

3. Install dependencies:

   ```bash
   python install.py
   ```

   On Windows you can simply execute `run.bat` to upgrade `pip`, install
   dependencies and launch the service in one step.  Logs are written to
   `log.log` in the repository root for troubleshooting.

## Configuration

Edit `config.json` to match your environment.  Important fields include the
Discord bot token and MongoDB connection details.  The dispatch ports can be
left at their defaults unless you are running multiple instances on the same
host.

Missing keys are automatically populated with sensible defaults and any
type mismatches are reported at startup.  Every option lives in this single
configuration file so changes propagate consistently across machines.

## Running on Multiple Machines

Each machine should have the repository and configuration file.  On
two or three machines the typical workflow is:

1. Ensure all machines can reach the MongoDB instance and have network access
   to the dispatch ports listed in `config.json`.
2. Start the services on each machine:

   ```bash
   python main.py
   ```

3. Any machine missing a Discord token will skip the bot but continue to
   process messages and dispatch outputs, allowing flexible deployment.

## Testing

To run a lightweight smoke test without launching the GUI:

```bash
python main.py --no-gui --test
```

## License

This project is provided as-is without a specific license.
