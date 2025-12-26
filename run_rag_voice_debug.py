# Debug wrapper for running rag_voice under Streamlit
# Install global exception handlers (sys, threading, asyncio) before importing
# so that exceptions raised in worker threads/processes are captured to a file.

import sys
import traceback
import threading
import asyncio

LOG_PATH = r"C:\VS Code Programs\voicechat\voicechat\rag_voice_runtime_error.log"

def _write_exc(exc_type, exc_value, exc_tb):
    try:
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    except Exception:
        # Best-effort; don't mask original exception
        pass

# sys.excepthook for uncaught exceptions in the main thread
sys.excepthook = _write_exc

# threading.excepthook for Python 3.8+
def _thread_excepthook(args):
    _write_exc(args.exc_type, args.exc_value, args.exc_traceback)

try:
    threading.excepthook = _thread_excepthook
except Exception:
    # Older Python versions may not have threading.excepthook
    pass

# asyncio exception handler
def _asyncio_exc_handler(loop, context):
    try:
        msg = context.get("message") or context
        # context may include the exception
        exc = context.get("exception")
        if exc is not None:
            tb = exc.__traceback__
            _write_exc(type(exc), exc, tb)
        else:
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                f.write(str(msg))
    except Exception:
        pass

try:
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(_asyncio_exc_handler)
except Exception:
    pass

try:
    import rag_voice

    if hasattr(rag_voice, "main"):
        rag_voice.main()
    else:
        # If rag_voice doesn't have a main(), just ensure module import happened
        pass
except Exception:
    # Write the traceback and re-raise so Streamlit/console also sees it
    _write_exc(*sys.exc_info())
    raise
