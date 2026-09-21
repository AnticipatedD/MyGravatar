terraform {
  required_version = ">= 1.5.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2.0"
    }
  }
}

module "gpu_cluster" {
  source     = "./modules/gpu-cluster"
  node_count = 2
}
