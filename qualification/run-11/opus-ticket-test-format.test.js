const test = require("node:test");
const assert = require("node:assert");
const { formatTotal } = require("../src/format");

test("order total shows currency code", () => {
  assert.strictEqual(formatTotal(12.5, "GBP"), "12.50 GBP");
});
