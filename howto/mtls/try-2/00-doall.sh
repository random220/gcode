rm -rf out
mkdir out
. 01-mkcakey
. 02-mkcacert
. 03-mksrvkey
. 04-mksrvcsr
. 05-mksrvcert
#06-startserver
. 07-mkclntkey
. 08-mkclntcsr
. 09-mkclntcert
#10-startserver-mtls
#11-curlclient

echo
echo
echo 'Add these to /etc/hosts'
echo '------------------------------------'
grep DNS out/server.cnf.1 |sed 's/^.*= */127.0.0.1 /'
echo '------------------------------------'


