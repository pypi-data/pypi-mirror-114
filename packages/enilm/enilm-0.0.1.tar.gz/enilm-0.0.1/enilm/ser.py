import io
import sys
from typing import List


def get_ports() -> List[str]:
    import serial.tools.list_ports
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    serial.tools.list_ports.main()
    ports = sys.stdout.getvalue().split()
    sys.stdout = original_stdout
    return ports
