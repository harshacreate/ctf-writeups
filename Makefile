.PHONY: test web crypto logs

test:
	python -m pytest

web:
	python -m challenges.web_access.app

crypto:
	python -m ctf_lab.crypto

logs:
	python -m ctf_lab.forensics
