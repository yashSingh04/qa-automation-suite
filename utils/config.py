"""Central test configuration, overridable by environment variables."""
import os


class Config:
    # --- Web UI ---
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "0"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")

    # --- API ---
    API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))

    # --- Mobile (Appium) ---
    APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
    PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")
    PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "")      # blank = any
    DEVICE_NAME = os.getenv("DEVICE_NAME", "Android Emulator")
    AUTOMATION_NAME = os.getenv("AUTOMATION_NAME", "UiAutomator2")
    APP_PATH = os.getenv("APP_PATH", "apps/ApiDemos-debug.apk")
    APP_PACKAGE = os.getenv("APP_PACKAGE", "io.appium.android.apis")
    APP_ACTIVITY = os.getenv("APP_ACTIVITY", ".ApiDemos")
    APPIUM_EXPLICIT_WAIT = int(os.getenv("APPIUM_EXPLICIT_WAIT", "20"))
    NEW_COMMAND_TIMEOUT = int(os.getenv("NEW_COMMAND_TIMEOUT", "120"))

    # --- Test data ---
    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    PROBLEM_USER = os.getenv("PROBLEM_USER", "problem_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
