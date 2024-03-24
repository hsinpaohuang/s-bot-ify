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

      expect(mockedFetch).toHaveBeenCalledTimes(1);
      expect(mockedFetch).toHaveBeenCalledWith('test', { method: 'post' });
      expect(result).toHaveProperty('data', mockedFetchResponseData);
    });
  });

  describe('authedFetch', async () => {
    const mockedGoto = mock();

    async function mockAuthStore() {
      await mock.module('$lib/stores/authStore', () => ({
        authStore: {
          isLoggedIn: true,
          accessToken: 'access_token',
          tokenType: 'token_type'
        },
      }));
    }

    // mocking this in beforeAll causes other tests to be affected
    function mockCamelizedFetch() {
      return spyOn(subjects, 'camelizedFetch')
        .mockImplementation(
          // @ts-expect-error mocking relevant properties only
          () => Promise.resolve({ data: mockedFetchResponseData }),
        );
    }

    const options = { headers: { Authorization: 'token_type access_token' } };

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

    it('correctly processes path params', async () => {
      await mockAuthStore();
      const mockedCamelizedFetch = mockCamelizedFetch();

      subjects.authedFetch('/pathWithSlash');
      subjects.authedFetch('pathWithoutSlash');
      subjects.authedFetch('https://PUBLIC_API_URL.com/api/fullURL');

      expect(mockedCamelizedFetch).toHaveBeenCalledTimes(3);
      expect(mockedCamelizedFetch).toHaveBeenNthCalledWith(
        1,
        'https://PUBLIC_API_URL.com/api/pathWithSlash',
        options,
      );
      expect(mockedCamelizedFetch).toHaveBeenNthCalledWith(
        2,
        'https://PUBLIC_API_URL.com/api/pathWithoutSlash',
        options,
      );
      expect(mockedCamelizedFetch).toHaveBeenNthCalledWith(
        3,
        'https://PUBLIC_API_URL.com/api/fullURL',
        options,
      );

      mockedCamelizedFetch.mockRestore();
    });

    it('adds auth headers and calls camelizedFetch', async () => {
      await mockAuthStore();
      const mockedCamelizedFetch = mockCamelizedFetch();

      const res = await subjects.authedFetch('test', { method: 'POST' });

      expect(mockedGoto).not.toHaveBeenCalled();
      expect(mockedCamelizedFetch).toHaveBeenCalledTimes(1);
      expect(mockedCamelizedFetch).toHaveBeenCalledWith(
        'https://PUBLIC_API_URL.com/api/test',
        { method: 'POST', ...options },
      );
      expect(res).toHaveProperty('data', mockedFetchResponseData);

      mockedCamelizedFetch.mockRestore();
    });
  });
});
