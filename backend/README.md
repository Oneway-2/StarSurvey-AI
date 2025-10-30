# Backend (FastAPI) - Azure App Service notes

This file explains how to run the `backend` FastAPI app on Azure App Service (Linux).

Why this file
- Oryx auto-detection sometimes picks the wrong framework (e.g., Flask) if there are multiple entrypoint-like files in the repo. To avoid that, set an explicit startup command.

Recommended approach (Azure Portal)
1. Deploy your repo as usual to an Azure App Service (Linux). Ensure `requirements.txt` is present so Oryx installs dependencies.
2. In the Azure Portal -> your App Service -> Settings -> Configuration -> General settings, set **Startup Command** to:

   /home/site/wwwroot/startup.sh

   (or directly: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`)

3. Save and restart the App Service.

What `startup.sh` does
- Changes to `/home/site/wwwroot`.
- Activates the Oryx-created virtual environment named `antenv` if it exists.
- Runs `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.

Alternate: Direct startup command
- If you prefer not to add `startup.sh`, set the Startup Command to:

  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --log-level info

Notes and troubleshooting
- If logs show "Detected an app based on Flask" and the service tries to run `gunicorn app:app`, it means Oryx misdetected the framework. Setting the Startup Command above overrides the auto-detection.
- If packages are not installed, confirm `requirements.txt` is at the repository root and `SCM_DO_BUILD_DURING_DEPLOYMENT` is enabled (default). Check the deployment logs for build errors.
- To debug locally, run:

  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

-- end
