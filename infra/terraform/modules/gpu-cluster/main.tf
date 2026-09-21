resource "null_resource" "amd_gpu_node" {
  count = var.node_count
}
