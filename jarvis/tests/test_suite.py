# ==================================================
# JARVIS AI — Unit & Integration Test Suite (unittest)
# ==================================================

import asyncio
import os
import sys
import tempfile
from pathlib import Path
import unittest

# Ensure root path is imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import jarvis.tools
from jarvis.config.constants import PermissionLevel, PermissionScope
from jarvis.core.brain import brain
from jarvis.core.permission_manager import PermissionManager
from jarvis.memory.long_term_memory import LongTermMemory
from jarvis.memory.short_term_memory import ShortTermMemory
from jarvis.tools.registry import tool_registry


class TestJarvisCore(unittest.IsolatedAsyncioTestCase):

    async def test_tool_registry_and_schemas(self):
        tools = tool_registry.list_tools()
        self.assertGreaterEqual(len(tools), 5)

        schemas = tool_registry.get_schemas()
        self.assertEqual(len(schemas), len(tools))

        tool_names = [t.name for t in tools]
        self.assertIn("open_application", tool_names)
        self.assertIn("browser_search", tool_names)
        self.assertIn("youtube_search", tool_names)
        self.assertIn("get_current_time", tool_names)
        self.assertIn("manage_memory", tool_names)

    async def test_time_tool(self):
        res = await tool_registry.execute("get_current_time")
        self.assertTrue(res.success)
        self.assertIn("The time is", res.message)

    async def test_memory_system(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mem_file = Path(tmp_dir) / "test_mem.json"
            ltm = LongTermMemory(storage_path=mem_file)

            item = ltm.add("User loves Python and Three.js")
            self.assertEqual(item["text"], "User loves Python and Three.js")

            results = ltm.search("Python")
            self.assertEqual(len(results), 1)

            success = ltm.remove(item["id"])
            self.assertTrue(success)
            self.assertEqual(len(ltm.all()), 0)

            stm = ShortTermMemory(max_turns=3)
            stm.add_turn("user", "Hello Jarvis")
            stm.add_turn("assistant", "Greetings Sir")
            self.assertEqual(len(stm.get_recent_turns()), 2)

    async def test_fast_intent_routing(self):
        # English commands
        r1 = brain.fast_route("open notepad")
        self.assertIsNotNone(r1)
        self.assertEqual(r1[0], "open_application")
        self.assertEqual(r1[1]["app_name"], "notepad")

        r2 = brain.fast_route("search youtube for machine learning tutorials")
        self.assertIsNotNone(r2)
        self.assertEqual(r2[0], "youtube_search")
        self.assertIn("machine learning", r2[1]["query"])

        # Hindi / Hinglish commands
        r3 = brain.fast_route("youtube pe python tutorial search karo")
        self.assertIsNotNone(r3)
        self.assertEqual(r3[0], "youtube_search")
        self.assertIn("python tutorial", r3[1]["query"])

        r4 = brain.fast_route("time kya hua")
        self.assertIsNotNone(r4)
        self.assertEqual(r4[0], "get_current_time")

    async def test_permission_manager(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            perm_file = Path(tmp_dir) / "test_perms.json"
            pm = PermissionManager(storage_path=perm_file)

            allowed = await pm.check_and_request(
                scopes=[PermissionScope.SCREEN_READ],
                action_description="Take screen capture",
            )
            self.assertTrue(allowed)

            pm.set_permission(PermissionScope.CAMERA, PermissionLevel.DENY)
            allowed_camera = await pm.check_and_request(
                scopes=[PermissionScope.CAMERA],
                action_description="Access webcam",
            )
            self.assertFalse(allowed_camera)


if __name__ == "__main__":
    unittest.main()
