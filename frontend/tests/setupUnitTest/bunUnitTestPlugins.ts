import { plugin } from "bun";

// reference: https://github.com/oven-sh/bun/issues/5541

plugin({
  name: "sveltekit-env",
  setup(build) {
    build.module('$app/navigation', () => ({
      exports: { goto: () => Promise.resolve(), },
      loader: 'object',
    })),
    build.module("$app/environment", () => ({
      exports: { browser: true },
      loader: 'object',
    }));
    build.module('$env/static/public', () => ({
      exports: { PUBLIC_API_URL: 'https://PUBLIC_API_URL.com' },
      loader: 'object',
    }));
  },
});
