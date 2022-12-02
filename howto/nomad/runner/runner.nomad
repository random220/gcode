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
