#!/bin/bash

mkdir .xx
cd .xx


docker run -d -p 6000:5000 --restart always --name registry registry
tmux new-session -d -s mynomad bash -c 'nomad agent -dev'
# To attach to it
# tmux a -t mynomad



cat >install.sh <<'EOF'
#!/bin/bash

apt-get -y update
apt-get -y dist-upgrade
apt-get -y install vim curl git sudo netcat
EOF

chmod a+x install.sh

cat >entry.sh <<'EOF'
#!/bin/bash

echo hi
echo hi
echo hi
while true; do
  sleep 1
done
EOF

chmod a+x entry.sh

cat >Dockerfile <<'EOF'
FROM ubuntu:20.04
COPY install.sh /
RUN /install.sh
COPY entry.sh /
CMD /entry.sh
EOF

docker build -t runner .
docker tag runner localhost:6000/runner
docker push localhost:6000/runner

cat >runner.nomad <<'EOF'
job "runner" {
  datacenters = ["dc1"]
  type = "service"
  group "runner" {
    count = 3
    network {
    }
    service {
      name = "runner"
      provider = "nomad"
    }
    task "runner" {
      driver = "docker"
      config {
        image = "localhost:6000/runner"
        auth_soft_fail = true
      }
      resources {
        cpu    = 500 # 500 MHz
        memory = 256 # 256MB
      }
    }
  }
}
EOF

nomad job run runner.nomad

