import { goto } from "$app/navigation";
import { PUBLIC_API_URL } from "$env/static/public";
import { authStore } from "$lib/stores/authStore";
import { recursivelyCamelize } from "$lib/utils/caseConversion";
import { HTTPStatusCode } from "$lib/utils/httpStatusCode";

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
 * Wrapper for `camelizedFetch`, but automatically adds authorization header,
 * and also does not require API endpoint origin
 *
 * Will redirect current page to `/login` if access token is missing
 *
 * @param path path, which will be concatenated to `PUBLIC_API_URL/api/`
 * @param options same as default fetch
 * @returns Same as from `camelizedFetch`
 *
 * @see camelizedFetch
 */
export async function authedFetch<S, F = undefined>(
  path: string,
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

  const url = path.startsWith(PUBLIC_API_URL)
    ? path
    : `${PUBLIC_API_URL}/api/${path.startsWith('/') ? path.slice(1) : path}`;

  const headers = Object.assign(
    { Authorization: `${tokenType} ${accessToken}` },
    options?.headers,
  );

  const res = await camelizedFetch<S, F>(url, { ...options, headers });

  if (res && res.status === HTTPStatusCode.Unauthorized) {
    await goto('/login');
    return;
  }

  return res;
}
