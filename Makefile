.PHONY: help setup auth demo demo-all demo-fast demo-pipeline demo-web demo-dashboard check-ingest real fetch-web ingest preprocess database train aqi hcho transport dashboard test lint clean

CONFIG    ?= config/config.yaml
# Fall back to `python` on Windows / environments where `python3` alias is absent
PY        ?= python

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	 awk 'BEGIN {FS=":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

setup:           ## Install Python package in editable mode & frontend dependencies
	pip install -e .
	pnpm install

auth:            ## Authenticate Google Earth Engine (one-time)
	earthengine authenticate

demo:            ## Run ALL-IN-ONE demo (web map + dashboard in one terminal; auto-generates data if needed)
	$(PY) scripts/run_demo.py

demo-all:        ## Re-run full pipeline simulation, then launch web map + dashboard
	$(PY) scripts/run_demo.py --pipeline

demo-web:        ## Launch only the Next.js web application (http://localhost:3000)
	$(PY) scripts/run_demo.py --no-dashboard

demo-dashboard:  ## Launch only the Streamlit research dashboard (http://localhost:8501)
	$(PY) scripts/run_demo.py --no-web

demo-pipeline:   ## Run the full synthetic pipeline & export web data (no servers)
	$(PY) pipelines/run_demo.py
	$(PY) pipelines/export_web.py

demo-fast:       ## Quick smoke run of synthetic pipeline & export web data (no servers)
	$(PY) pipelines/run_demo.py --fast
	$(PY) pipelines/export_web.py

check-ingest:    ## Show which ingestion deps / credentials / inputs are ready
	$(PY) pipelines/check_ingest.py

fetch-web:       ## Pull REAL TROPOMI/MODIS/ERA5 observation layers into the web app (no CPCB needed)
	$(PY) pipelines/fetch_real_web.py

real:            ## ONE-COMMAND real run: fetch GEE predictors + (with CPCB in data/external) train+validate -> real AQI
	$(PY) pipelines/run_real.py

ingest:          ## Phase 2: download all datasets (GEE + INSAT/MOSDAC + CPCB)
	$(PY) pipelines/01_ingest.py --config $(CONFIG)

preprocess:      ## Phase 4: regrid, QA-filter, temporally aggregate, collocate
	$(PY) pipelines/02_preprocess.py --config $(CONFIG)

database:        ## Phase 3: assemble the unified India-wide training table
	$(PY) pipelines/03_build_database.py --config $(CONFIG)

train:           ## Phases 6-7: train RF/XGB baselines (CNN-LSTM training lives in run_demo.py)
	$(PY) pipelines/04_train.py --config $(CONFIG)

aqi:             ## [scaffold] Phases 5,8,9 stub — the real AQI run is `make demo` / `make real`
	$(PY) pipelines/05_generate_aqi.py --config $(CONFIG)

hcho:            ## [scaffold] Phases 10,11 stub — the real HCHO run is `make demo` / `make fetch-web`
	$(PY) pipelines/06_hcho_analysis.py --config $(CONFIG)

transport:       ## [scaffold] Phase 13 stub — the real transport run is `make demo` / `make fetch-web`
	$(PY) pipelines/07_transport.py --config $(CONFIG)

dashboard:       ## Launch the Streamlit dashboard
	streamlit run dashboard/app.py

test:            ## Run unit tests (AQI engine, PHV, Getis-Ord are fully tested)
	pytest -q

lint:            ## Lint with ruff
	ruff check src pipelines tests

clean:           ## Remove caches and interim artifacts
	$(PY) scripts/clean.py
