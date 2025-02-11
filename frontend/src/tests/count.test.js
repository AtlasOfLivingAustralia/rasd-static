import { expect, test } from 'vitest';

//Basic test to make sure Vitest works. Will delete when first unit tests are written.

test('useCounter', () => {
  let count = 0;
  expect(count).toBe(0);
  count++;
  expect(count).toBe(1);
});
