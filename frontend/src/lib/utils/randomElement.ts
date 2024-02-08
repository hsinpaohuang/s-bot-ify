/** returns a random element from the given array */
export function randomElement<T>(from: T[]) {
  return from[Math.floor(Math.random() * from.length)];
}
