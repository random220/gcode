I'm glad you found the information helpful! Configuring Nginx for advanced use cases like mutual TLS with specific client certificate restrictions can indeed be complex and may not be well-documented in a single place. Here are a few additional tips and resources that might help you further:

### Additional Tips

1. **Nginx Documentation**:
   - The official Nginx documentation is a great resource for understanding the various directives and their usage. You can find it [here](https://nginx.org/en/docs/).

2. **Community and Forums**:
   - Websites like Stack Overflow, Server Fault, and the Nginx mailing list can be very helpful for specific questions and troubleshooting.

3. **Books**:
   - Books like "Nginx HTTP Server" by Clément Nedelcu and "Mastering Nginx" by Dimitri Aivaliotis provide in-depth coverage of Nginx configuration and advanced use cases.

4. **Online Tutorials**:
   - Websites like DigitalOcean, Linode, and various tech blogs often have step-by-step tutorials for configuring Nginx for different scenarios.

### Example Configuration with Detailed Comments

Here's the example configuration with additional comments for clarity:

```nginx
http {
    # Map the requested URI to the expected client certificate CN
    map $request_uri $expected_cn {
        default "";  # Default value if no match is found
        ~^/app1/api/v1 "aaaa.713205.cccc";  # Match for /app1/api/v1
        ~^/app2/api/v1 "bbbb.713205.dddd";  # Match for /app2/api/v1
    }

    server {
        listen 443 ssl;
        server_name your_server_name;

        # SSL certificate and key for the server
        ssl_certificate /path/to/server-cert.pem;
        ssl_certificate_key /path/to/server-key.pem;

        # CA certificate to verify client certificates
        ssl_client_certificate /path/to/ca-cert.pem;
        ssl_verify_client on;  # Enable client certificate verification

        location / {
            # Check if the client certificate CN matches the expected CN
            if ($ssl_client_s_dn_cn != $expected_cn) {
                return 403;  # Return 403 Forbidden if CN does not match
            }

            # Proxy the request to the backend server
            proxy_pass http://your_backend_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

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

- **Logging**: Enable logging to troubleshoot any issues with client certificate verification. Add the following lines to the `server` block to enable detailed logging:

  ```nginx
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;
  ```

- **Security**: Ensure that the certificate files are properly secured and have the appropriate permissions to prevent unauthorized access.

By following these steps and tips, you can configure Nginx to handle complex scenarios like mutual TLS with specific client certificate restrictions effectively. If you have more questions or need further assistance, feel free to ask!