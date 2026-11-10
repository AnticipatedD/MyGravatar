resource "null_resource" "amd_gpu_node" {
  count = var.node_count

  triggers = {
    node_index    = tostring(count.index)
    instance_type = var.instance_type
  }
}
