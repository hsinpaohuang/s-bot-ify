import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  mock,
  spyOn,
} from "bun:test";
import * as subjects from "$lib/utils/fetchWrappers";
import type { recursivelyCamelize } from "$lib/utils/caseConversion";

describe('fetchWrappers', () => {
  const mockedRecursivelyCamelize = mock(
    (obj: Parameters<typeof recursivelyCamelize>) => obj,
  );
  const mockedFetch = spyOn(window, 'fetch').mockImplementation(
    // @ts-expect-error mocking relevant properties only
    () => Promise.resolve({ json: () => mockedFetchResponseData }),
  );;

  const mockedFetchResponseData = { hello_world: 'foo' };

  beforeAll(async () => {
    await mock.module('$lib/utils/caseConversion', () => ({
      recursivelyCamelize: mockedRecursivelyCamelize,
    }));
  });

  afterEach(() => {
    mockedRecursivelyCamelize.mockClear();
    mockedFetch.mockClear();
  });

  afterAll(() => {
    mockedRecursivelyCamelize.mockRestore();
    mockedFetch.mockRestore();
    mock.restore();
  });

  describe('camelizedFetch', () => {
    it('calls recursivelyCamelize to transform response body', async () => {
      await subjects.camelizedFetch('test');

      expect(mockedRecursivelyCamelize).toHaveBeenCalledTimes(1);
    });

    it('passes params to fetch correctly', async () => {
      const result = await subjects.camelizedFetch('test', { method: 'post' });

      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith('test', { method: 'post' });
      expect(result).toHaveProperty('data', mockedFetchResponseData);
    });
  });

  describe('authedFetch', async () => {
    const mockedGoto = mock();

    beforeAll(async () => {
      mock.module('$app/navigation', () => ({ goto: mockedGoto }));
    });

    afterEach(() => {
      mockedGoto.mockClear();
    });

    it('redirects to /login if user is not logged in', async () => {
      await mock.module('$lib/stores/authStore', () => ({
        authStore: { isLoggedIn: false },
      }));

      await subjects.authedFetch('test');

      expect(mockedGoto).toHaveBeenCalledTimes(1);
      expect(mockedGoto).toHaveBeenCalledWith('/login');
    });

    it('adds auth headers and calls camelizedFetch', async () => {
      await mock.module('$lib/stores/authStore', () => ({
        authStore: {
          isLoggedIn: true,
          accessToken: 'access_token',
          tokenType: 'token_type'
        },
      }));

      const mockedCamelizedFetch = spyOn(subjects, 'camelizedFetch')
        .mockImplementation(
          // @ts-expect-error mocking relevant properties only
          () => Promise.resolve({ data: mockedFetchResponseData }),
        );

      const res = await subjects.authedFetch('test', { method: 'POST' });

      expect(mockedGoto).not.toHaveBeenCalled();
      expect(mockedCamelizedFetch).toHaveBeenCalledWith(
        'test',
        {
          method: 'POST',
          headers: { Authorization: 'token_type access_token' },
        },
      );
      expect(res).toHaveProperty('data', mockedFetchResponseData);
    });
  });
});
