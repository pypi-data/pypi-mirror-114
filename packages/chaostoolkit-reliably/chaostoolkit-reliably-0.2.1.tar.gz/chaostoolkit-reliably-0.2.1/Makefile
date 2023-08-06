.PHONY: lint
lint:
	flake8 chaosreliably/ tests/ examples/
	isort --check-only --profile black chaosreliably/ tests/ examples/
	black --check --diff chaosreliably/ tests/ examples/

.PHONY: format
format:
	isort --profile black chaosreliably/ tests/ examples/
	black chaosreliably/ tests/ examples/
