# Spotify Client

This client requires a `refresh_token` to be able to get the current track playing.

Recently Spotify changed the policy of refresh tokens, so you need to generate a new one. To do that you need to follow the following flow (Authorization Code Flow):

1. Generate an authentication `code`
    * Make a request to: `GET https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8080%2Fcallback&scope=user-read-currently-playing%20user-read-playback-state`. This will open an authorization webpage in your browser and you will need to agree on the terms. After that the URL address in your browser will be updated with the Spotify's response (including the code parameter).
1. Generate a token
    * Make a request to: `POST https://accounts.spotify.com/api/token` with url-form parameters: `grant_type=authorization_code&code={code}&redirect_uri=http%3A%2`
1. From the response of step 2 use the `refresh_token` to generate a new token.

