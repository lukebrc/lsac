import scalaparser

parser = scalaparser.ScalaParser()
#lines = '''class A {
#    private var _a: A = null
#}'''.split('\n')

lines = '''class A() {
}'''.split('\n')

objMap = parser.parseClasses(lines)
assert('A' in objMap)
assert('_a' in objMap['A'])
