Yes, you can configure Nginx to accept different client certificates based on the requested URL path. To achieve this, you can use the `map` directive to create a mapping between the requested URL path and the expected client certificate CN. Then, use this mapping in the `location` blocks to enforce the restrictions.

Here's an example Nginx configuration that demonstrates how to do this:

```nginx
http {
    map $request_uri $expected_cn {
        default "";
        ~^/app1/api/v1 "aaaa.713205.cccc";
        ~^/app2/api/v1 "bbbb.713205.dddd";
    }

    server {
        listen 443 ssl;
        server_name your_server_name;

        ssl_certificate /path/to/server-cert.pem;
        ssl_certificate_key /path/to/server-key.pem;
        ssl_client_certificate /path/to/ca-cert.pem;
        ssl_verify_client on;

        location / {
            if ($ssl_client_s_dn_cn != $expected_cn) {
                return 403;
            }

            proxy_pass http://your_backend_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Explanation

1. **Map Directive**:
   - The `map` directive creates a mapping between the requested URL path (`$request_uri`) and the expected client certificate CN (`$expected_cn`).
   - The `default` value is set to an empty string, which means that by default, no specific CN is expected.
   - The `~^/app1/api/v1` and `~^/app2/api/v1` patterns match the respective URL paths and set the expected CN accordingly.

2. **Location Block**:
   - The `if ($ssl_client_s_dn_cn != $expected_cn)` condition checks if the client certificate's CN matches the expected CN for the requested URL path. If it does not match, a `403 Forbidden` status is returned.
   - The `proxy_pass` directive specifies the backend server to which the request should be proxied.
   - The `proxy_set_header` directives set additional headers for the proxied request.

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

By following these steps, you can configure Nginx to accept different client certificates based on the requested URL path, enforcing the restrictions as specified.