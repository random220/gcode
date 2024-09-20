To configure an Nginx reverse proxy to enforce mutual TLS (mTLS) and restrict access based on the client certificate's Common Name (CN), you can use the following steps:

1. **Install Nginx with OpenSSL**:
   Ensure that Nginx is installed with OpenSSL support. On most systems, this is the default configuration.

2. **Prepare the Certificates**:
   Ensure you have the following certificate files:
   - `server-key.pem`: The server's private key.
   - `server-cert.pem`: The server's certificate.
   - `ca-cert.pem`: The CA certificate used to verify client certificates.

3. **Configure Nginx**:
   Edit the Nginx configuration file to enable mTLS and restrict access based on the client certificate's CN.

Here's an example Nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name your_server_name;

    ssl_certificate /path/to/server-cert.pem;
    ssl_certificate_key /path/to/server-key.pem;
    ssl_client_certificate /path/to/ca-cert.pem;
    ssl_verify_client on;

    location / {
        if ($ssl_client_s_dn_cn != "My Name is Khan!") {
            return 403;
        }

        proxy_pass http://your_backend_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Explanation

1. **SSL Configuration**:
   - `ssl_certificate`: Specifies the server's certificate.
   - `ssl_certificate_key`: Specifies the server's private key.
   - `ssl_client_certificate`: Specifies the CA certificate used to verify client certificates.
   - `ssl_verify_client on`: Enables client certificate verification.

2. **Location Block**:
   - `if ($ssl_client_s_dn_cn != "aaaa.713205.cccc")`: Checks if the client certificate's CN matches the expected value. If it does not match, a `403 Forbidden` status is returned.
   - `proxy_pass`: Specifies the backend server to which the request should be proxied.
   - `proxy_set_header`: Sets additional headers for the proxied request.

### Steps to Apply the Configuration

1. **Edit the Nginx Configuration File**:
   Open the Nginx configuration file (usually located at `/etc/nginx/nginx.conf` or in the `/etc/nginx/sites-available/` directory) and add the above configuration.

2. **Test the Nginx Configuration**:
   Before reloading Nginx, test the configuration for syntax errors:

   ```sh
   sudo nginx -t
   ```

3. **Reload Nginx**:
   If the configuration test is successful, reload Nginx to apply the changes:

   ```sh
   sudo systemctl reload nginx
   ```

### Additional Considerations

- **Logging**: You may want to enable logging to troubleshoot any issues with client certificate verification. Add the following lines to the `server` block to enable detailed logging:

  ```nginx
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;
  ```

- **Security**: Ensure that the certificate files are properly secured and have the appropriate permissions to prevent unauthorized access.

By following these steps, you can configure an Nginx reverse proxy to enforce mutual TLS and restrict access based on the client certificate's CN.
