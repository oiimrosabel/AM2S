import re
from pathlib import Path

from AM2S.display.DisplayTools import DisplayTools as Dt
from AM2S.errors.ProcedureError import ProcedureError
from AM2S.misc.NodeTools import NodeTools as Nt
from AM2S.procedure.Procedure import Procedure


class DoomProcedure(Procedure):
    def apply(self, path: Path):
        if path.suffix != ".doom":
            return path
        Dt.info("DoomProcedure launched")
        parentWad = ""
        with path.open('r') as f:
            data = f.read()
            res = re.match(r'parentwad "(.+?)"', data)
            if res is None or res.group(1) is None:
                raise ProcedureError(f'Invalid .doom file: {path}')
            parentWad = res.group(1)
            f.close()
        iwadPath = Nt.getFile(path.parent / ".IWAD" / parentWad)
        Dt.info(f"{path.name} references {iwadPath}")
        return iwadPath
