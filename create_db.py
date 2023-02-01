import contextlib
import time
import threading
import uvicorn

from app import main


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self, _time: int = 1e-3):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(_time)
            yield
        finally:
            self.should_exit = True
            thread.join()


config = uvicorn.Config(main.app, host="127.0.0.1", port=5000, log_level="info")
server = Server(config=config)

with server.run_in_thread():
    ...
