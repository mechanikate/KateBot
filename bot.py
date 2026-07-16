import asyncio, discord, os, pathlib, time

from discord.ext import commands

class KateBot(commands.Bot):
    _watcher: asyncio.Task

    def __init__(self, ext_dir: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ext_dir = pathlib.Path(ext_dir)

    async def _load_extensions(self):
        print("* loading exts...")
        for file in self.ext_dir.rglob("*.py"):
            if file.stem.startswith("_"):
                continue
            try:
                await self.load_extension(".".join(file.with_suffix("").parts))
                print(f"\\--> [PASS] loaded ext {file}")
            except commands.ExtensionError as e:
                print(f"\\--> [FAIL] failed to load ext {file} with error {e}")

    async def setup_hook(self):
        await self._load_extensions()
        self._watcher = self.loop.create_task(self._cog_watcher())

    async def _cog_watcher(self):
        print("* watching for changes...")
        last = time.time()
        while 1:
            extensions: set[str] = set()
            for name, module in self.extensions.items():
                if module.__file__ and os.stat(module.__file__).st_mtime > last:
                    extensions.add(name)
            for ext in extensions:
                try:
                    await self.reload_extension(ext)
                    print(f"\\--> [PASS] reloaded ext {ext}")
                except commands.ExtensionError as e:
                    print(f"\\--> [FAIL] failed to reload ext {ext} with error {e}")
            last = time.time()
            await asyncio.sleep(1)

intents = discord.Intents.default()
intents.message_content = True

KateBot("cogs/", command_prefix="kb!", intents = intents).run(os.environ["BOT_SECRET"])
