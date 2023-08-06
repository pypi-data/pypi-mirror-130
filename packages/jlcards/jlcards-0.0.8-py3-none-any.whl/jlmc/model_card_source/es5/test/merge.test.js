"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var cellslice_1 = require("../cellslice");
var log_slicer_1 = require("../log-slicer");
var slice_1 = require("../slice");
var testcell_1 = require("./testcell");
describe("SlicedExecution", function () {
    function cell(executionEventId, text, executionCount, id) {
        if (executionCount === undefined)
            executionCount = 1;
        return new testcell_1.TestCell(text, executionCount, executionEventId, id);
    }
    function cellSlice(cell, slice) {
        return new cellslice_1.CellSlice(cell, slice);
    }
    function location(first_line, first_column, last_line, last_column) {
        return {
            first_line: first_line,
            first_column: first_column,
            last_line: last_line,
            last_column: last_column
        };
    }
    function slicedExecution() {
        var cellSlices = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            cellSlices[_i] = arguments[_i];
        }
        return new log_slicer_1.SlicedExecution(new Date(), cellSlices);
    }
    describe("merge", function () {
        it("unions slices with different cells", function () {
            var slice1 = slicedExecution(cellSlice(cell("1", "a = 1", 1), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("2", "b = 2", 2), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var merged = slice1.merge(slice2);
            expect(merged.cellSlices[0].cell.executionEventId).toBe("1");
            expect(merged.cellSlices[1].cell.executionEventId).toBe("2");
        });
        it("will not include the same locations from the same cell twice", function () {
            var slice1 = slicedExecution(cellSlice(cell("1", "a = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("1", "a = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var merged = slice1.merge(slice2);
            expect(merged.cellSlices).toHaveLength(1);
            expect(merged.cellSlices[0].slice.size).toBe(1);
        });
        it("considers two cells sharing ID and execution count but differing in execution event " +
            "ID to be different", function () {
            var slice1 = slicedExecution(cellSlice(cell("1", "a = 1", 1, "id1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("2", "a = 1", 1, "id1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var merged = slice1.merge(slice2);
            expect(merged.cellSlices.length).toBe(2);
        });
        it("will include complementary ranges from two slices of the same cell", function () {
            var slice1 = slicedExecution(cellSlice(cell("1", "a = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("1", "a = 1"), new slice_1.LocationSet(location(1, 0, 1, 4))));
            var merged = slice1.merge(slice2);
            expect(merged.cellSlices).toHaveLength(1);
            expect(merged.cellSlices[0].slice.size).toBe(2);
            expect(merged.cellSlices[0].slice.items).toContainEqual(location(1, 0, 1, 5));
            expect(merged.cellSlices[0].slice.items).toContainEqual(location(1, 0, 1, 4));
        });
        it("reorders the cells in execution order", function () {
            var slice1 = slicedExecution(cellSlice(cell("2", "a = 1", 2), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("1", "a = 1", 1), new slice_1.LocationSet(location(1, 0, 1, 4))));
            var merged = slice1.merge(slice2);
            expect(merged.cellSlices[0].cell.executionCount).toBe(1);
            expect(merged.cellSlices[1].cell.executionCount).toBe(2);
        });
        it("can do an n-way merge with a bunch of cells", function () {
            var slice1 = slicedExecution(cellSlice(cell("1", "a = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))), cellSlice(cell("2", "b = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice2 = slicedExecution(cellSlice(cell("3", "c = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))), cellSlice(cell("4", "d = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var slice3 = slicedExecution(cellSlice(cell("5", "e = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))), cellSlice(cell("6", "f = 1"), new slice_1.LocationSet(location(1, 0, 1, 5))));
            var merged = slice1.merge(slice2, slice3);
            expect(merged.cellSlices).toHaveLength(6);
        });
    });
});
//# sourceMappingURL=merge.test.js.map