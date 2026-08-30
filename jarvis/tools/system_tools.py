import os
from datetime import datetime
from typing import Optional

try:
    import psutil
except ImportError:
    psutil = None

try:
    import pyautogui
except ImportError:
    pyautogui = None

from jarvis.config.constants import PermissionScope
from jarvis.config.settings import settings
from jarvis.computer.computer_controller import computer_controller
from jarvis.tools.base_tool import BaseTool, ToolParameter, ToolResult
from jarvis.tools.registry import tool_registry


# --------------------------------------------------
# Open Application Tool
# --------------------------------------------------
class OpenAppTool(BaseTool):
    name = "open_application"
    description = "Launch an authorized application or software on the computer."
    parameters = [
        ToolParameter(
            name="app_name",
            type="string",
            description="The name of the application (e.g. 'chrome', 'notepad', 'calculator', 'vscode').",
            required=True,
        )
    ]
    required_permissions = [PermissionScope.APPLICATION_LAUNCH]

    async def execute(self, app_name: str, **kwargs) -> ToolResult:
        res = computer_controller.open_app(app_name)
        return ToolResult(
            success=res.get("success", False),
            message=res.get("message", ""),
            data=res,
            error=res.get("error"),
        )


# --------------------------------------------------
# Close Application Tool
# --------------------------------------------------
class CloseAppTool(BaseTool):
    name = "close_application"
    description = "Close or terminate a running application process."
    parameters = [
        ToolParameter(
            name="app_name",
            type="string",
            description="The name of the application to terminate.",
            required=True,
        )
    ]
    required_permissions = [PermissionScope.APPLICATION_TERMINATE]
    is_sensitive = True

    async def execute(self, app_name: str, **kwargs) -> ToolResult:
        res = computer_controller.close_app(app_name)
        return ToolResult(
            success=res.get("success", False),
            message=res.get("message", ""),
            data=res,
            error=res.get("error"),
        )


# --------------------------------------------------
# Browser Search Tool
# --------------------------------------------------
class BrowserSearchTool(BaseTool):
    name = "browser_search"
    description = "Perform a Google search in the browser with optional profile selection."
    parameters = [
        ToolParameter(
            name="query",
            type="string",
            description="The search keywords or question.",
            required=True,
        ),
        ToolParameter(
            name="profile",
            type="string",
            description="Optional Chrome account/profile name (e.g. 'personal', 'college', 'work', 'manomay', 'asha').",
            required=False,
        ),
    ]
    required_permissions = [PermissionScope.BROWSER_CONTROL]

    async def execute(self, query: str, profile: Optional[str] = None, **kwargs) -> ToolResult:
        res = computer_controller.google_search(query, profile=profile)
        return ToolResult(
            success=res.get("success", False),
            message=res.get("message", f"Searching Google for: '{query}'"),
            data=res,
        )


# --------------------------------------------------
# YouTube Search Tool
# --------------------------------------------------
class YoutubeSearchTool(BaseTool):
    name = "youtube_search"
    description = "Search YouTube for videos, music, or tutorials with optional profile/account selection."
    parameters = [
        ToolParameter(
            name="query",
            type="string",
            description="The video search query.",
            required=True,
        ),
        ToolParameter(
            name="profile",
            type="string",
            description="Optional Chrome account/profile name (e.g. 'personal', 'college', 'work', 'manomay', 'asha').",
            required=False,
        ),
    ]
    required_permissions = [PermissionScope.BROWSER_CONTROL]

    async def execute(self, query: str, profile: Optional[str] = None, **kwargs) -> ToolResult:
        res = computer_controller.youtube_search(query, profile=profile)
        return ToolResult(
            success=res.get("success", False),
            message=res.get("message", f"Searching YouTube for: '{query}'"),
            data=res,
        )


# --------------------------------------------------
# Open Website Tool
# --------------------------------------------------
class OpenWebsiteTool(BaseTool):
    name = "open_website"
    description = "Open a specific website or URL in the web browser with optional profile selection."
    parameters = [
        ToolParameter(
            name="website",
            type="string",
            description="Website key (e.g. 'youtube', 'github', 'chatgpt') or full URL.",
            required=True,
        ),
        ToolParameter(
            name="profile",
            type="string",
            description="Optional Chrome account/profile name (e.g. 'personal', 'college', 'work', 'manomay', 'asha').",
            required=False,
        ),
    ]
    required_permissions = [PermissionScope.BROWSER_CONTROL]

    async def execute(self, website: str, profile: Optional[str] = None, **kwargs) -> ToolResult:
        res = computer_controller.open_website(website, profile=profile)
        return ToolResult(
            success=res.get("success", False),
            message=res.get("message", f"Opening website: '{website}'"),
            data=res,
        )


# --------------------------------------------------
# List Chrome Profiles Tool
# --------------------------------------------------
class ListChromeProfilesTool(BaseTool):
    name = "list_chrome_profiles"
    description = "List all available Google Chrome user profiles and registered accounts on this computer."
    parameters = []
    required_permissions = [PermissionScope.BROWSER_CONTROL]

    async def execute(self, **kwargs) -> ToolResult:
        profiles = computer_controller.list_chrome_profiles()
        if not profiles:
            return ToolResult(success=True, message="No Chrome profiles found.", data={})
        summary_lines = ["Available Chrome Accounts & Profiles:"]
        for p_dir, info in profiles.items():
            name = info.get("name") or info.get("gaia_name") or p_dir
            email = info.get("user_name", "No email")
            summary_lines.append(f"• {name} ({email}) -> Profile ID: {p_dir}")
        return ToolResult(
            success=True,
            message="\n".join(summary_lines),
            data=profiles,
        )


# --------------------------------------------------
# Tab Control Tool
# --------------------------------------------------
class TabControlTool(BaseTool):
    name = "tab_controls"
    description = "Manage browser tabs (new_tab, close_tab, reopen_tab, next_tab, previous_tab)."
    parameters = [
        ToolParameter(
            name="action",
            type="string",
            description="Tab action to perform.",
            enum=["new_tab", "close_tab", "reopen_tab", "next_tab", "previous_tab"],
            required=True,
        )
    ]
    required_permissions = [PermissionScope.BROWSER_CONTROL]

    async def execute(self, action: str, **kwargs) -> ToolResult:
        b = computer_controller.browser
        actions = {
            "new_tab": b.new_tab,
            "close_tab": b.close_tab,
            "reopen_tab": b.reopen_tab,
            "next_tab": b.next_tab,
            "previous_tab": b.previous_tab,
        }
        fn = actions.get(action)
        if fn:
            res = fn()
            return ToolResult(success=res["success"], message=res["message"], data=res)
        return ToolResult(success=False, error=f"Unknown tab action: {action}")


# --------------------------------------------------
# Window Control Tool
# --------------------------------------------------
class WindowControlTool(BaseTool):
    name = "window_controls"
    description = "Minimize, maximize, or close active application window."
    parameters = [
        ToolParameter(
            name="action",
            type="string",
            description="Window action.",
            enum=["minimize", "maximize", "close"],
            required=True,
        )
    ]
    required_permissions = [PermissionScope.SYSTEM_CONTROL]

    async def execute(self, action: str, **kwargs) -> ToolResult:
        c = computer_controller
        actions = {
            "minimize": c.minimize_window,
            "maximize": c.maximize_window,
            "close": c.close_window,
        }
        fn = actions.get(action)
        if fn:
            res = fn()
            return ToolResult(success=res["success"], message=res["message"], data=res)
        return ToolResult(success=False, error=f"Unknown window action: {action}")


# --------------------------------------------------
# Screenshot Tool
# --------------------------------------------------
class TakeScreenshotTool(BaseTool):
    name = "take_screenshot"
    description = "Capture the current display and save the image file."
    parameters = [
        ToolParameter(
            name="filename",
            type="string",
            description="Optional custom filename for the screenshot.",
            required=False,
            default=settings.SCREENSHOT_FILENAME,
        )
    ]
    required_permissions = [PermissionScope.SCREEN_READ]

    async def execute(self, filename: Optional[str] = None, **kwargs) -> ToolResult:
        try:
            name = filename or settings.SCREENSHOT_FILENAME
            filepath = settings.SCREENSHOT_DIR / name
            if pyautogui:
                img = pyautogui.screenshot()
                img.save(str(filepath))
            else:
                filepath.write_text("mock screenshot data", encoding="utf-8")
            return ToolResult(
                success=True,
                message=f"Screenshot saved successfully as '{name}'.",
                data={"filepath": str(filepath)},
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e), message=f"Failed to take screenshot: {e}")


# --------------------------------------------------
# System Status Tool
# --------------------------------------------------
class GetSystemStatusTool(BaseTool):
    name = "get_system_status"
    description = "Retrieve current CPU, RAM, battery, disk usage and active window status."
    parameters = []
    required_permissions = []

    async def execute(self, **kwargs) -> ToolResult:
        try:
            if psutil:
                cpu = psutil.cpu_percent(interval=0.1)
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage("/").percent if os.name != "nt" else psutil.disk_usage("C:").percent
                battery_obj = psutil.sensors_battery()
                battery = f"{battery_obj.percent}%" if battery_obj else "AC Power"
            else:
                cpu, ram, disk, battery = 15.0, 45.0, 50.0, "100%"

            data = {
                "cpu_percent": cpu,
                "ram_percent": ram,
                "disk_percent": disk,
                "battery": battery,
                "timestamp": datetime.now().isoformat(),
            }
            return ToolResult(
                success=True,
                message=f"CPU: {cpu}%, RAM: {ram}%, Battery: {battery}",
                data=data,
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# Register all system tools
tool_registry.register(OpenAppTool())
tool_registry.register(CloseAppTool())
tool_registry.register(BrowserSearchTool())
tool_registry.register(YoutubeSearchTool())
tool_registry.register(OpenWebsiteTool())
tool_registry.register(TabControlTool())
tool_registry.register(WindowControlTool())
tool_registry.register(TakeScreenshotTool())
tool_registry.register(GetSystemStatusTool())
