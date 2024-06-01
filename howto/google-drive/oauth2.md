# OAuth 2.0 flow

OAuth 2.0 is a protocol that allows a user to grant a third-party application access to their resources on another service, without sharing their login credentials.

Here's a simplified explanation of the flow:

1. **Registration**: The third-party application (often called the "client") registers with the service (the "resource server") that the user uses. The service provides the client with a client ID and a client secret.

2. **Authorization Request**: When the user wants to use the client application with their service, the client directs the user to an authorization endpoint on the service. The user logs in (if they aren't already) and the endpoint asks the user if they want to allow the client to access their resources. This request includes the client ID, the types of access being requested (the "scopes"), and a redirect URI.

3. **Authorization Grant**: If the user agrees, the authorization server (which might be the same as the resource server) provides an authorization grant, which is a temporary code. This code is sent to the client via the redirect URI.

4. **Access Token Request**: The client then makes a request to the authorization server's token endpoint to exchange the authorization code for an access token. This request includes the client ID, the client secret, and the authorization code.

5. **Access Token**: The authorization server verifies the request and, if it's valid, provides the client with an access token. This token is what the client will use to access the user's resources.

6. **Resource Request**: The client then makes a request to the resource server, including the access token in the request.

7. **Resource Access**: The resource server verifies the access token and, if it's valid, provides the requested resources to the client.

This flow is known as the "Authorization Code Grant" flow, which is commonly used for server-side applications. There are other flows for different types of clients, like single-page applications or mobile apps.


**Question: Thanks for the lucid explanation. Really helpful.
So, who gets to see the client-id and the client secret?**


You're welcome! I'm glad I could help.

The client ID and client secret are both issued to the third-party application (the "client") by the service (the "authorization server") during the registration process.

The client ID is not a secret; it's often embedded in URLs and can be seen by the user and other parties. It's used to identify the client to the authorization server.

The client secret, on the other hand, is a secret known only to the authorization server and the client. The client should keep it confidential and not share it with anyone, including the user. It's used to authenticate the client to the authorization server when requesting an access token.

In some cases, where the client is a public client (like a client-side web application or a native application), a client secret is not used, because it can't be reliably kept confidential in these types of clients.

**My usecase is a public client. A javascript app to run in a browser. The service is google drive API. The user is whoever loads the html code in the browser. What are my options?**

If your use case involves a public client, such as a JavaScript application running in a browser, and you're using the Google Drive API, the recommended OAuth 2.0 flow is the "Implicit Grant" flow.

Here's a simplified explanation of the flow:

1. **Registration**: You register your application with Google's OAuth 2.0 server. You'll receive a client ID and, optionally, a client secret (which you won't need for the Implicit Grant flow).

2. **Authorization Request**: When the user wants to use your application with their Google Drive, your application directs the user to an authorization endpoint on Google's OAuth 2.0 server. The user logs in (if they aren't already) and the endpoint asks the user if they want to allow your application to access their resources. This request includes the client ID, the types of access being requested (the "scopes"), and a redirect URI.

3. **Access Token**: If the user agrees, the authorization server doesn't provide an authorization code. Instead, it immediately provides an access token. This token is included in the URL fragment (the part of the URL after the '#') when the user is redirected to the redirect URI.

4. **Access Token Extraction**: Your application extracts the access token from the URL fragment. Because the URL fragment is not sent to the server when the browser makes a request, the access token is not exposed to the server, which is important for security in a public client.

5. **Resource Request**: Your application then makes a request to the Google Drive API, including the access token in the request.

6. **Resource Access**: The Google Drive API verifies the access token and, if it's valid, provides the requested resources to your application.

The Implicit Grant flow is designed for clients where the client secret can't be reliably kept confidential. The access token is exposed to the user and any other party that can see the user's browser history, so it should have a short lifetime and limited permissions.
