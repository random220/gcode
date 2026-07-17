http://cloud.oracle.com/
login

See all your vms here
https://cloud.oracle.com/compute/instances

See all your used resources (including vms) here
https://cloud.oracle.com/?region=us-ashburn-1

Make port 8484 avaialble to internet
Click on one of your vms
Click Networking (second item on top horizontal menu)
Look for the subnet name. Click on that. psub1 in my example.
Click on Security menu item on top horizontal menu
You'll see something like "Default Security List for vcn1", click that
Click on "Security rules"
Add an ingress rule reading
    Source: 0.0.0.0/0 (for every ip address), 206.248.82.112/32 (just that one),
            206.248.82.112/31 (112 and 113), 206.248.82.112/30 (112,113,114,115)
    IP Protocol: TCP
    Source Port Range: All
    Destination Port Range: 8484

And then open firewall port on the OS of the VM
    $ sudo firewall-cmd --add-port=8484/tcp --permanent
    $ sudo firewall-cmd --reload

