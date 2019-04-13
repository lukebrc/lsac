import scalaparser

parser = scalaparser.ScalaParser()
lines = '''class A {
    private var _a: A = null
}'''.split('\n')
objMap = parser.parseClasses(lines, 0)
assert('A' in objMap)
assert('_a' in objMap['A'])
