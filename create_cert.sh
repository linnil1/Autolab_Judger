mkdir -p web/certs
cd web/certs
openssl genrsa 4096 > privkey.pem
chmod 400 privkey.pem
openssl req -new -x509 -nodes -sha1 -days 365 -key privkey.pem -out fullchain.pem
cd ../..
