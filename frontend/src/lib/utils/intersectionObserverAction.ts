/** @type {import('svelte/action').Action}  */
export function intersectionObserver(
  node: HTMLElement,
  options?: IntersectionObserverInit,
) {
  let observer = makeObserver(node, options);
  observer.observe(node);

  function update(newOptions?: IntersectionObserverInit) {
    observer.disconnect();
    observer = makeObserver(node, newOptions);
    observer.observe(node);
  }

  function destroy() {
    observer.disconnect();
  }

  return { update, destroy };
}

function makeObserver(node: HTMLElement, options?: IntersectionObserverInit) {
  return new IntersectionObserver(
    ([{ isIntersecting }]) => {
      node.dispatchEvent(new CustomEvent<boolean>(
        'intersect',
        { detail: isIntersecting },
      ));
    },
    options,
  );
}
