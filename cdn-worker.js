addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

function formatTimestamp(timestampInSeconds = Date.now()) {
  const date = new Date(timestampInSeconds * 1000); // Convert seconds to milliseconds

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

async function handleRequest(request) {
  const path = new URL(request.url).pathname;
  const targetUrl = `https://cdnb.jonasjones.dev${path}`;
  const response = await fetch(targetUrl);

  // Check if the response status is 404
  if (response.status === 404 /*|| response.status === 522*/) {
    console.log("404 error. the path is" + path)
    console.log(response)
    // If it's a 404, show a custom 404 page
    return new Response('404 File not found.', {
      status: 404,
      error: "Not Found",
      message: "The requested resource could not be found.",
      details: "Resource " + path.split('/')[path.split('/').length - 1] + "not found.",
      timestamp: formatTimestamp(),
      path: path
    }
    ,
    );
  }

  // If it's not a 404, perform the redirect
  //return Response.redirect(targetUrl, 302); // You can use 301 for a permanent redirect if needed
  return response;
}
