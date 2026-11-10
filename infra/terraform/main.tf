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
  source = "./modules/gpu-cluster"

  node_count    = 2
  instance_type = "gpu.amd.mi300x"
}

output "cluster_node_ids" {
  value       = module.gpu_cluster.cluster_node_ids
  description = "Terraform resource identifiers for the GPU node slots."
}

output "cluster_size" {
  value       = module.gpu_cluster.cluster_size
  description = "Configured number of GPU node slots."
}
