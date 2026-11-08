variable "node_count" {
  type        = number
  description = "Number of AMD GPU nodes in the cluster"
  default     = 2
}

variable "instance_type" {
  type        = string
  description = "Instance type for the AMD GPU nodes"
  default     = "gpu.amd.mi300x"
}

resource "null_resource" "amd_gpu_node" {
  count = var.node_count

  triggers = {
    node_index    = count.index
    instance_type = var.instance_type
  }
}

output "cluster_node_ids" {
  value       = null_resource.amd_gpu_node[*].id
  description = "List of IDs for the provisioned AMD GPU nodes"
}

output "cluster_size" {
  value       = var.node_count
  description = "Total number of nodes in the GPU cluster"
}
