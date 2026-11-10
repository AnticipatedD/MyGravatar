output "cluster_node_ids" {
  value       = null_resource.amd_gpu_node[*].id
  description = "Terraform identifiers for the GPU node placeholder resources."
}

output "cluster_size" {
  value       = var.node_count
  description = "Configured number of GPU node slots."
}
