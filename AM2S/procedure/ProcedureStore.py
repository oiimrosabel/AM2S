from AM2S.procedure.DefaultProcedure import DefaultProcedure
from AM2S.procedure.DoomProcedure import DoomProcedure
from AM2S.procedure.ZipProcedure import ZipProcedure

strToProcedures = {
    "default": DefaultProcedure(),
    "zip": ZipProcedure(),
    "doom": DoomProcedure()
}
