export function buildApiUrl(apiRoute: string): string {
  // Get the current location (e.g., 'localhost' or 'example.com')
  const { hostname } = window.location;

  // Construct the URL using the 'http' protocol, the current hostname, port 5000, and the given API route
  const url = new URL(`http://${hostname}:5010/api/${apiRoute}`);

  return url.toString();
}
