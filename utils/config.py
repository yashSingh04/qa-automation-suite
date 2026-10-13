"""Central test configuration, overridable by environment variables."""
import os


class Config:
    # --- UI ---
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "0"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")

    # --- API ---
    API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

    # --- Test data ---
    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    PROBLEM_USER = os.getenv("PROBLEM_USER", "problem_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
