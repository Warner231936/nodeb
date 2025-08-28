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


## Progress
### Completed
- Added GUI queue display and chaos log.
- Discord bot now forwards all messages for analysis.
- Database connection respects configuration-defined database name.

- Self-state checks CPU/memory usage and maintenance mode to gate engagement.

- Placeholder self-state module integrated into engagement logic.
- Repaired self-state availability check to ensure runtime gating works.


### In Progress
- Integrating real LLM models and refining database storage.
- Refining engagement logic with self-state insights.

### Next Steps
- Expand engagement logic and persistence once LLM integration stabilizes.
- Add unit tests for database and engagement modules.
- Implement full self-state tracking and resource-based response control.
