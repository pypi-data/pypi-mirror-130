"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var control_flow_1 = require("../control-flow");
var data_flow_1 = require("../data-flow");
var printNode_1 = require("../printNode");
var python_parser_1 = require("../python-parser");
var specs_1 = require("../specs");
describe("detects dataflow dependencies", function () {
    function analyze() {
        var codeLines = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            codeLines[_i] = arguments[_i];
        }
        var code = codeLines.concat("").join("\n"); // add newlines to end of every line.
        var analyzer = new data_flow_1.DataflowAnalyzer();
        printNode_1.printNode;
        return analyzer.analyze(new control_flow_1.ControlFlowGraph(python_parser_1.parse(code))).dataflows;
    }
    function analyzeLineDeps() {
        var codeLines = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            codeLines[_i] = arguments[_i];
        }
        return analyze.apply(void 0, codeLines).items.map(function (dep) { return [
            dep.toNode.location.first_line,
            dep.fromNode.location.first_line
        ]; });
    }
    it("from variable uses to names", function () {
        var deps = analyzeLineDeps("a = 1", "b = a");
        expect(deps).toContainEqual([2, 1]);
    });
    it("handles multiple statements per line", function () {
        var deps = analyzeLineDeps("a = 1", "b = a; c = b", "d = c");
        expect(deps).toContainEqual([2, 1]);
        expect(deps).toContainEqual([3, 2]);
    });
    it("only links from a use to its most recent def", function () {
        var deps = analyzeLineDeps("a = 2", "a.prop = 3", "a = 4", "b = a");
        expect(deps).toContainEqual([4, 3]);
        expect(deps).not.toContainEqual([4, 1]);
    });
    it("handles augmenting assignment", function () {
        var deps = analyzeLineDeps("a = 2", "a += 3");
        expect(deps).toContainEqual([2, 1]);
    });
    it("links between statements, not symbol locations", function () {
        var deps = analyze("a = 1", "b = a");
        expect(deps.items[0].fromNode.location).toEqual({
            first_line: 1,
            first_column: 0,
            last_line: 1,
            last_column: 5
        });
        expect(deps.items[0].toNode.location).toEqual({
            first_line: 2,
            first_column: 0,
            last_line: 2,
            last_column: 5
        });
    });
    it("links to a multi-line dependency", function () {
        var deps = analyze("a = func(", "    1)", "b = a");
        expect(deps.items[0].fromNode.location).toEqual({
            first_line: 1,
            first_column: 0,
            last_line: 2,
            last_column: 6
        });
    });
    it("to a full for-loop declaration", function () {
        var deps = analyze("for i in range(a, b):", "    print(i)");
        expect(deps.items[0].fromNode.location).toEqual({
            first_line: 1,
            first_column: 0,
            last_line: 1,
            last_column: 21
        });
    });
    it("links from a class use to its def", function () {
        var deps = analyzeLineDeps("class C(object):", "    pass", "", "c = C()");
        expect(deps).toEqual([[4, 1]]);
    });
    it("links from a function use to its def", function () {
        var deps = analyzeLineDeps("def func():", "    pass", "", "func()");
        expect(deps).toEqual([[4, 1]]);
    });
});
describe("detects control dependencies", function () {
    function analyze() {
        var codeLines = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            codeLines[_i] = arguments[_i];
        }
        var code = codeLines.concat("").join("\n"); // add newlines to end of every line.
        var deps = [];
        new control_flow_1.ControlFlowGraph(python_parser_1.parse(code)).visitControlDependencies(function (control, stmt) {
            return deps.push([stmt.location.first_line, control.location.first_line]);
        });
        return deps;
    }
    it("to an if-statement", function () {
        var deps = analyze("if cond:", "    print(a)");
        expect(deps).toEqual([[2, 1]]);
    });
    it("for multiple statements in a block", function () {
        var deps = analyze("if cond:", "    print(a)", "    print(b)");
        expect(deps).toEqual([[2, 1], [3, 1]]);
    });
    it("from an else to an if", function () {
        var deps = analyze("if cond:", "    print(a)", "elif cond2:", "    print(b)", "else:", "    print(b)");
        expect(deps).toContainEqual([3, 1]);
        expect(deps).toContainEqual([5, 3]);
    });
    it("not from a join to an if-condition", function () {
        var deps = analyze("if cond:", "    print(a)", "print(b)");
        expect(deps).toEqual([[2, 1]]);
    });
    it("not from a join to a for-loop", function () {
        var deps = analyze("for i in range(10):", "    print(a)", "print(b)");
        expect(deps).toEqual([[2, 1]]);
    });
    it("to a for-loop", function () {
        var deps = analyze("for i in range(10):", "    print(a)");
        expect(deps).toContainEqual([2, 1]);
    });
    it("skipping non-dependencies", function () {
        var deps = analyze("a = 1", "b = 2");
        expect(deps).toEqual([]);
    });
});
describe("getDefs", function () {
    function getDefsFromStatements(moduleMap) {
        var codeLines = [];
        for (var _i = 1; _i < arguments.length; _i++) {
            codeLines[_i - 1] = arguments[_i];
        }
        var code = codeLines.concat("").join("\n");
        var module = python_parser_1.parse(code);
        var options = createDataflowOptionsForModuleMap(moduleMap);
        var analyzer = new data_flow_1.DataflowAnalyzer(options);
        return module.code.reduce(function (refSet, stmt) {
            var refs = analyzer.getDefs(stmt, refSet);
            return refSet.union(refs);
        }, new data_flow_1.RefSet()).items;
    }
    function getDefsFromStatement(code, mmap) {
        mmap = mmap || specs_1.DefaultSpecs;
        code = code + "\n"; // programs need to end with newline
        var mod = python_parser_1.parse(code);
        var options = createDataflowOptionsForModuleMap(mmap);
        var analyzer = new data_flow_1.DataflowAnalyzer(options);
        return analyzer.getDefs(mod.code[0], new data_flow_1.RefSet()).items;
    }
    function getDefNamesFromStatement(code, mmap) {
        return getDefsFromStatement(code, mmap).map(function (def) { return def.name; });
    }
    function createDataflowOptionsForModuleMap(moduleMap) {
        var options;
        if (moduleMap) {
            options = {
                symbolTable: {
                    loadDefaultModuleMap: false,
                    moduleMap: moduleMap
                }
            };
        }
        return options;
    }
    describe("detects definitions", function () {
        it("for assignments", function () {
            var defs = getDefsFromStatement("a = 1");
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.VARIABLE,
                name: "a",
                level: data_flow_1.ReferenceType.DEFINITION
            });
        });
        it("for augmenting assignments", function () {
            var defs = getDefsFromStatement("a += 1");
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.VARIABLE,
                name: "a",
                level: data_flow_1.ReferenceType.UPDATE
            });
        });
        it("for imports", function () {
            var defs = getDefsFromStatement("import pandas");
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.IMPORT,
                name: "pandas"
            });
        });
        it("for from-imports", function () {
            var defs = getDefsFromStatement("from pandas import load_csv");
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.IMPORT,
                name: "load_csv"
            });
        });
        it("for function declarations", function () {
            var defs = getDefsFromStatement(["def func():", "    return 0"].join("\n"));
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.FUNCTION,
                name: "func",
                location: {
                    first_line: 1,
                    first_column: 0,
                    last_line: 4,
                    last_column: -1
                }
            });
        });
        it("for class declarations", function () {
            var defs = getDefsFromStatement(["class C(object):", "    def __init__(self):", "        pass"].join("\n"));
            expect(defs[0]).toMatchObject({
                type: data_flow_1.SymbolType.CLASS,
                name: "C",
                location: {
                    first_line: 1,
                    first_column: 0,
                    last_line: 5,
                    last_column: -1
                }
            });
        });
        describe("that are weak (marked as updates)", function () {
            it("for dictionary assignments", function () {
                var defs = getDefsFromStatement(["d['a'] = 1"].join("\n"));
                expect(defs.length).toBe(1);
                expect(defs[0].level).toBe(data_flow_1.ReferenceType.UPDATE);
                expect(defs[0].name).toBe("d");
            });
            it("for property assignments", function () {
                var defs = getDefsFromStatement(["obj.a = 1"].join("\n"));
                expect(defs.length).toBe(1);
                expect(defs[0].level).toBe(data_flow_1.ReferenceType.UPDATE);
                expect(defs[0].name).toBe("obj");
            });
        });
        describe("from annotations", function () {
            it("from our def annotations", function () {
                var defs = getDefsFromStatement('"""defs: [{ "name": "a", "pos": [[0, 0], [0, 11]] }]"""%some_magic');
                expect(defs[0]).toMatchObject({
                    type: data_flow_1.SymbolType.MAGIC,
                    name: "a",
                    location: {
                        first_line: 1,
                        first_column: 0,
                        last_line: 1,
                        last_column: 11
                    }
                });
            });
            it("computing the def location relative to the line it appears on", function () {
                var defs = getDefsFromStatements(undefined, "# this is an empty line", '"""defs: [{ "name": "a", "pos": [[0, 0], [0, 11]] }]"""%some_magic');
                expect(defs[0]).toMatchObject({
                    location: {
                        first_line: 2,
                        first_column: 0,
                        last_line: 2,
                        last_column: 11
                    }
                });
            });
        });
        describe("including", function () {
            it("function arguments", function () {
                var defs = getDefNamesFromStatement("func(a)");
                expect(defs.length).toBe(1);
            });
            it("the object a function is called on", function () {
                var defs = getDefNamesFromStatement("obj.func()");
                expect(defs.length).toBe(1);
            });
        });
        describe("; given a spec,", function () {
            it("can ignore all arguments", function () {
                var defs = getDefsFromStatement("func(a, b, c)", {
                    __builtins__: { functions: ["func"] }
                });
                expect(defs).toEqual([]);
            });
            it("assumes arguments have side-effects, without a spec", function () {
                var defs = getDefsFromStatement("func(a, b, c)", {
                    __builtins__: { functions: [] }
                });
                expect(defs).not.toBeUndefined();
                expect(defs.length).toBe(3);
                var names = defs.map(function (d) { return d.name; });
                expect(names).toContain("a");
                expect(names).toContain("b");
                expect(names).toContain("c");
            });
            it("can ignore the method receiver", function () {
                var specs = { __builtins__: { types: { C: { methods: ["m"] } } } };
                var defs = getDefsFromStatements(specs, "x=C()", "x.m()");
                expect(defs).not.toBeUndefined();
                expect(defs.length).toBe(1);
                expect(defs[0].name).toContain("x");
                expect(defs[0].level).toContain(data_flow_1.ReferenceType.DEFINITION);
            });
            it("assumes method call affects the receiver, without a spec", function () {
                var specs = { __builtins__: {} };
                var defs = getDefsFromStatements(specs, "x=C()", "x.m()");
                expect(defs).not.toBeUndefined();
                expect(defs.length).toBe(2);
                expect(defs[1].name).toBe("x");
                expect(defs[1].level).toBe(data_flow_1.ReferenceType.UPDATE);
            });
            it("can process a class name as both a type and function", function () {
                var CType = { methods: [{ name: "m", reads: [], updates: [0] }] };
                var specs = {
                    __builtins__: {
                        types: { C: CType },
                        functions: [{ name: "C", returns: "C" }]
                    }
                };
                var defs = getDefsFromStatements(specs, "x=C()");
                expect(defs).not.toBeUndefined();
                expect(defs.length).toBe(1);
                expect(defs[0].name).toBe("x");
                expect(defs[0].inferredType).toEqual(CType);
            });
        });
    });
    describe("doesn't detect definitions", function () {
        it("for names used outside a function call", function () {
            var defs = getDefNamesFromStatement("a + func()");
            expect(defs).toEqual([]);
        });
        it("for functions called early in a call chain", function () {
            var defs = getDefNamesFromStatement("func().func()");
            expect(defs).toEqual([]);
        });
    });
});
describe("getUses", function () {
    function getUseNames() {
        var codeLines = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            codeLines[_i] = arguments[_i];
        }
        var code = codeLines.concat("").join("\n");
        var mod = python_parser_1.parse(code);
        var analyzer = new data_flow_1.DataflowAnalyzer();
        return analyzer.getUses(mod.code[0]).items.map(function (use) { return use.name; });
    }
    describe("detects uses", function () {
        it("of functions", function () {
            var uses = getUseNames("func()");
            expect(uses).toContain("func");
        });
        it("for undefined symbols in functions", function () {
            var uses = getUseNames("def func(arg):", "    print(a)");
            expect(uses).toContain("a");
        });
        it("handles augassign", function () {
            var uses = getUseNames("x -= 1");
            expect(uses).toContain("x");
        });
        it("of functions inside classes", function () {
            var uses = getUseNames("class Baz():", "  def quux(self):", "    func()");
            expect(uses).toContain("func");
        });
        it("of variables inside classes", function () {
            var uses = getUseNames("class Baz():", "  def quux(self):", "    self.data = a");
            expect(uses).toContain("a");
        });
        it("of functions and variables inside nested classes", function () {
            var uses = getUseNames("class Bar():", "  class Baz():", "    class Qux():", "      def quux(self):", "         func()", "         self.data = a");
            expect(uses).toContain("func");
            expect(uses).toContain("a");
        });
    });
    describe("ignores uses", function () {
        it("for symbols defined within functions", function () {
            var uses = getUseNames("def func(arg):", "    print(arg)", "    var = 1", "    print(var)");
            expect(uses).not.toContain("arg");
            expect(uses).not.toContain("var");
        });
        it("for params used in an instance function body", function () {
            var uses = getUseNames("class Foo():", "    def func(arg1):", "        print(arg1)");
            expect(uses).not.toContain("arg1");
        });
    });
});
//# sourceMappingURL=analysis.test.js.map