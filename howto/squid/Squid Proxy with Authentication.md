# Squid Proxy with Authentication


Sure, I can guide you through the process of configuring Squid proxy on Ubuntu to serve only certain clients based on authentication. Here are the steps:

1. **Install Squid Proxy**: First, you need to install Squid if it's not already installed. You can do this by running the following command in your terminal:

   ```
   sudo apt-get update
   sudo apt-get install squid
   ```

2. **Configure Squid**: The main configuration file for Squid is located at `/etc/squid/squid.conf`. You can open this file with your preferred text editor. For example, you can use nano:

   ```
   sudo nano /etc/squid/squid.conf
   ```

3. **Set up Access Control Lists (ACLs)**: In the Squid configuration file, you can define Access Control Lists (ACLs) to control which clients can access the proxy. Here's an example of how to set up an ACL for authenticated users:

   ```
   acl authenticated_users proxy_auth REQUIRED
   http_access allow authenticated_users
   ```

   This configuration allows only users who provide valid authentication credentials to use the proxy.

4. **Set up Authentication**: Squid uses external helpers for authentication. You can use the `Basic` authentication scheme with the `NCSA` helper, which checks passwords stored in a plain text file. Here's how to set it up:

   - First, create a password file:

     ```
     sudo htpasswd -c /etc/squid/passwd your_username
     ```

     You'll be prompted to enter a password for the user.

   - Then, add the following lines to your `squid.conf` file:

     ```
     auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwd
     auth_param basic children 5
     auth_param basic realm Squid proxy-caching web server
     auth_param basic credentialsttl 2 hours
     ```

5. **Restart Squid**: After making changes to the configuration file, you need to restart Squid for the changes to take effect:

   ```
   sudo systemctl restart squid
   ```

Remember to replace `your_username` with the actual username you want to use. Also, the path to the `basic_ncsa_auth` helper might be different depending on your system.

This is a basic setup that should get you started. You might need to adjust the configuration depending on your specific requirements. For more detailed information, you can refer to the official Squid documentation.