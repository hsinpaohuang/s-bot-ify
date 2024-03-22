import { it, describe, expect } from 'bun:test';
import { recursivelyCamelize } from '$lib/utils/caseConversion';

describe('caseConversion', () => {
  describe('recursivelyCamelize', () => {
    it('throws error if param is not an object or array', () => {
      // @ts-expect-error testing incorrect param
      expect(() => recursivelyCamelize('123')).toThrow();
      // @ts-expect-error testing incorrect param
      expect(() => recursivelyCamelize(123)).toThrow();
      // @ts-expect-error testing incorrect param
      expect(() => recursivelyCamelize(true)).toThrow();
      // @ts-expect-error testing incorrect param
      expect(() => recursivelyCamelize(null)).toThrow();
      // @ts-expect-error testing incorrect param
      expect(() => recursivelyCamelize(undefined)).toThrow();

      expect(() => recursivelyCamelize([] as unknown[])).not.toThrow();
      expect(() => recursivelyCamelize({})).not.toThrow();
    });

    it('returns camelized object', () => {
      expect(recursivelyCamelize({
        hello_world: 'hello world',
        foo: { bar_baz: 'foo bar baz' },
      })).toEqual({
        helloWorld: 'hello world',
        foo: { barBaz: 'foo bar baz' },
      });
    });

    it('returns array of primitives without any modifications', () => {
      expect(recursivelyCamelize([1, '2', true, null, undefined])).toEqual(
        [1, '2', true, null, undefined],
      )
    });

    it('returns array of objects with camelized keys', () => {
      expect(
        recursivelyCamelize([{ hello_world: 'hello world', foo_bar: 'baz' }]),
      ).toEqual([{ helloWorld: 'hello world', fooBar: 'baz' }]);
    });
  });
});
