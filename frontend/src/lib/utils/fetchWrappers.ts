import { goto } from "$app/navigation";
import { authStore } from "$lib/stores/authStore";
import { recursivelyCamelize } from "$lib/utils/caseConversion";

type ResponseWithData<T> = Omit<
  Response & { data?: T },
  'arrayBuffer' | 'blob' | 'formData' | 'json' | 'text'
>;

type ResponseWithSuccessData<T> = ResponseWithData<T> & { ok: true };

type ResponseWithFailedData<T> = ResponseWithData<T> & { ok: false };

/**
 * Wrapper for native `fetch`, but recursively camelizes response data keys
 * Only use this for responses with body as JSON format
 *
 * @param url URL string
 * @param options same as default fetch
 * @returns `Response` with property `data`,
 * which holds the response body parsed with `res.json` and with recursively camelized keys
 *
 * @see fetch
 */
export async function camelizedFetch<S, F = undefined>(
  url: string | URL | Request,
  options?: FetchRequestInit,
): Promise<ResponseWithSuccessData<S> | ResponseWithFailedData<F>> {
  const res = await fetch(url, options);

  const data = recursivelyCamelize(await res.json());
  Object.assign(res, { data });

  return res;
}

/**
 * Wrapper for `camelizedFetch`, but automatically adds authorization header.
 *
 * Will redirect current page to `/login` if access token is missing
 *
 * @param url URL string
 * @param options same as default fetch
 * @returns Same as from `camelizedFetch`
 *
 * @see camelizedFetch
 */
export async function authedFetch<S, F = undefined>(
  url: string | URL | Request,
  options?: FetchRequestInit,
): Promise<
  ResponseWithSuccessData<S>
  | ResponseWithFailedData<F>
  | undefined
> {
  const { isLoggedIn, accessToken, tokenType } = authStore;

  if (!isLoggedIn) {
    await goto('/login');
    return;
  }

  const headers = Object.assign(
    { Authorization: `${tokenType} ${accessToken}` },
    options?.headers,
  );

  return await camelizedFetch(url, { ...options, headers });
}
