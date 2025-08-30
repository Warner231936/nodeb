# Agent Instructions
- Run `python -m py_compile $(git ls-files '*.py')` before committing.
- Run `python main.py --no-gui --test` to smoke test the services.
- Use clear, maintainable code.
- Add suggestions here for future sessions.

## Suggestions
- Consider adding comprehensive unit tests for each module.
- Implement full reflection and long-term memory modules.
- Introduce graceful shutdown for services and database connections.
- Develop comprehensive self-state monitoring to inform engagement decisions.
- Extend self-state metrics to track disk and network pressure.
- Persist dispatched outputs for auditing and user review.

- Enhance Discord message sanitization and request auditing.

- Add retries and timeout handling for external reflection service.

- Automate multi-machine deployment and configuration validation.
- Expand configuration validation with type checks and defaults.
- Provide automated model downloads and checksum validation to ensure LLM availability.


## Progress
### Completed
- Added GUI queue display and chaos log.
- Discord bot now forwards all messages for analysis.
- Database connection respects configuration-defined database name.

- GUI now shows final responses and logs errors via popup message boxes.

- Self-state checks CPU/memory usage and maintenance mode to gate engagement.

- Placeholder self-state module integrated into engagement logic.
- Repaired self-state availability check to ensure runtime gating works.

- Discord bot sanitizes messages and handles `!req` commands case-insensitively.

- Installer upgrades pip and requirements; main runner validates config and optional Discord token.
- GUI uses dark glitchcore theme with neon accents.
- README documents multi-machine setup.
- Configuration-driven settings consolidated; added remote listener and MongoDB installer script.
- Config loader warns about missing keys to aid troubleshooting.
- Loader now auto-fills defaults and verifies value types.

### In Progress
- Integrating real LLM models and refining database storage.
- Refining engagement logic with self-state insights.

### Next Steps
- Expand engagement logic and persistence once LLM integration stabilizes.
- Add unit tests for database and engagement modules.
- Implement full self-state tracking and resource-based response control.
- Store dispatched outputs for later review and improve error recovery.

### Session Notes
- Done: expanded config loader with defaults and type checks; enhanced README with Windows batch launcher details.
- Worked on: configuration handling and documentation polish.
- Partially done: broader configuration validation schema.
- Next: add unit tests for configuration logic.
- Estimated completion: 30%

- Done: added config auto-generation and listener fallbacks; documented system fallback behavior.
- Worked on: strengthening error handling across configuration and listener scripts.
- Partially done: broader fallback coverage for remaining modules.
- Next: extend fallbacks to LLM operations and create unit tests.
- Estimated completion: 35%

- Done: implemented LLM offline mode and per-package installer retries; updated README.
- Worked on: broader fallback support for model startup and dependency installation.
- Partially done: automated model retrieval and comprehensive installer logging.
- Next: add tests for installer fallback and integrate real models.
- Estimated completion: 40%
