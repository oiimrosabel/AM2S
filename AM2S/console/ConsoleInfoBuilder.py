from AM2S.console.ConsoleInfo import ConsoleInfo
from AM2S.procedure.ProcedureStore import strToProcedures
from AM2S.templates.Builder import Builder


class ConsoleInfoBuilder(Builder):
    __entry: dict

    def __init__(self, entry: dict):
        self.__entry = entry

    def build(self) -> ConsoleInfo:
        procedureName = self.__entry.get('procedure', "default")
        procedureObj = strToProcedures.get(procedureName, None)

        return ConsoleInfo(
            id=self.__entry.get("id", 0),
            suffixes=self.__entry.get("format", []),
            preferredWidth=self.__entry.get("width", 0),
            genericName=self.__entry.get("generic", ""),
            procedure=procedureObj
        )
