import { transform, camelCase, isObject } from 'lodash-es';

/**
 * Recursively converts the keys of the given objects to camelCase.
 * @param obj object to be converted. Will error if it's not an object or array
 * @returns Object with camelCase keys
 * @see https://stackoverflow.com/a/59771233
 */
export function recursivelyCamelize<
  TResult extends unknown[] | Record<string, unknown>,
  T = unknown[] | Record<string, unknown>,
>(obj: T): TResult {
  if (!Array.isArray(obj) && !isObject(obj)) {
    throw new Error(
      `recursivelyCamelize only accepts array or objects, got ${typeof obj}.`,
    );
  }

  return transform<T, TResult>(
    // @ts-expect-error too difficult to correctly annotate type
    obj,
    (acc, value, key, target) => {
      // @ts-expect-error too difficult to correctly annotate type
      const camelizedKey = Array.isArray(target) ? key : camelCase(key);

      // @ts-expect-error too difficult to correctly annotate type
      acc[camelizedKey] = isObject(value) ? recursivelyCamelize(value) : value;
    },
  );
}
