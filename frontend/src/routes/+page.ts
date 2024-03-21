import { redirect } from '@sveltejs/kit';

// TODO: add landing page
// temporarily redirect users to /login until there is a landing page
export function load() {
  redirect(307, '/login');
}
