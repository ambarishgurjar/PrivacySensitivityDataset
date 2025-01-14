from chatgpt_wrapper.chatgpt import AsyncChatGPT
from chatgpt_wrapper.gpt_shell import GPTShell

class BrowserShell(GPTShell):


    def configure_commands(self):
        self.commands = self._introspect_commands(__class__)

    async def configure_backend(self):
        self.backend = await AsyncChatGPT(self.config).create(timeout=90)

    async def do_session(self, _):

        await self.backend.refresh_session()
        usable = (
            "The session appears to be usable."
            if "accessToken" in self.backend.session
            else "The session is not usable.  Try `install` mode."
        )
        self._print_markdown(f"* Session information refreshed.  {usable}")

    async def cleanup(self):
        await self.backend.cleanup()