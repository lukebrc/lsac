from object_map import ObjectMap
from grammar.gword import GWord
from grammar.gname import GName
from grammar.bracket_exp import BracketExp
from grammar.gsequence import GSequence
from grammar.gany import GAny
import re


SCALA_TYPE = GSequence( [GWord(":"), GName] )

DEFINITIONS = [
    GSequence( [GWord("class"), GName(), BracketExp("(", ")"), BracketExp("{", "}") ] ),
    GSequence( [GWord("def"), GName(), BracketExp("(", ")"), GOptional(SCALA_TYPE), BracketExp("{", "}") ] ),
    GSequence( [GAny()] )
]

class ScalaFileParser(object):
    def __init__(self, lines):
        self._lines = lines
        self._definitions = DEFINITIONS
        #self._objMap = ObjectMap()
        #self._currentClass = ''
        #self._i = 0

    def parseObjects(self):
        self._currentClass = ''
        self._i = 0
        while self._i < len(self._lines):
            self._parseLine(self._lines[self._i])
        return self._objMap

    def _parseLine(self, line):
        line = self._lines[self._i]
        if ScalaFileParser._isClassDef(line):
            self._currentClass = ScalaFileParser._getClassName(line)
            self._objMap.addClass(self._currentClass)
            if line.find('(') != -1:
                while line.find(')') == -1:
                    if self._i+1 >= len(lines):
                        break
                    line += lines[self._i+1]
                    self._i += 1
                self._parseClassArguments(self._currentClass, line)
        elif ScalaFileParser._isFunDef(line):
            if line.find('(') != -1:
                while line.find(')') == -1:
                    if self._i+1 < len(lines):
                        break
                    line += lines[self._i+1]
                    self._i += 1
            funId = ScalaFileParser._parseFunDef(line)
            self._objMap.addFunction(self._currentClass, funId)
        elif ScalaFileParser._isVarDef(line):
            varName, varType = ScalaFileParser._parseVarDef(line)
            self._objMap.addVar(self._currentClass, varName)
        self._i += 1

    def _parseClassArguments(self, className, line):
        r1 = re.findall(r"\s*class\s+(\w+)(.*)", line)
        argsStr = r1[0][1]
        for arg in argsStr.split(','):
            argName, argType = ScalaFileParser._parseArgDecl(arg)
            self._objMap.addVar(className, argName)

    @staticmethod
    def _parseArgDecl(argStr):
        if argStr.find(':') == -1:
            return argStr, ''
        r1 = re.findall(r"\s*(\w+)\s*:\s*(\w+)", argStr)
        return r1[0][0], r1[0][1]

    @staticmethod
    def _parseFunDef(line):
        r1 = re.findall(r"\s*(private|public)*\s*def (\w+\s*\(.*\))",
                        line)
        return r1[0][1]

    @staticmethod
    def _parseVarDef(line):
        r1 = re.findall(r"\s*(private|public)?\s+va[rl]\s+(\w+)", line)
        if len(r1) == 0:
            return None, None
        varName = r1[0][-1]
        varType = ScalaFileParser._getVarType(line)
        return varName, varType

    @staticmethod
    def _getVarType(line):
        r1 = re.findall(r"\s*(\w+)\s*:\s*(\w+)\s*", line)
        if len(r1) != 0:
            return r1[0][1]
        r1 = re.findall(r"\s*(\w+)\s*=\s*new\s+(\w+)", line)
        if len(r1) != 0:
            return r1[0][1]
        r1 = re.findall(r"\s*(\w+)\s*=\s*(\w+)\(.*\)", line)
        if len(r1) != 0:
            return r1[0][1]
        return None

    @staticmethod
    def _isClassDef(line):
        return re.match(r"\s*(class|object)\s+(\w+)", line)

    @staticmethod
    def _getClassName(line):
        match = re.findall(r"\s*class\s+(\w+)", line)
        if len(match) == 0:
            match = re.findall(r"\s*object\s+(\w+)", line)
        return match[0]

    @staticmethod
    def _isFunDef(line):
        return re.match(r"\s*(private|public)?\s*def \w+\s*\(.*\)", line)

    @staticmethod
    def _isVarDef(line):
        r1 = re.findall(r"\s*va[rl]\s+(\w+)(\s*:\s*\w+)?\s*=(.*)", line)
        return len(r1) > 0


