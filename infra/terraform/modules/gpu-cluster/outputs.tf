output "node_ids" {
  value = null_resource.amd_gpu_node[*].id
}
