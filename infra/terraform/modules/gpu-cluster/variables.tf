variable "node_count" {
  type        = number
  description = "Number of AMD GPU node slots."
  default     = 2

  validation {
    condition = (
      var.node_count >= 1 &&
      floor(var.node_count) == var.node_count
    )

    error_message = "node_count must be a positive integer."
  }
}

variable "instance_type" {
  type        = string
  description = "Configured AMD GPU instance type."
  default     = "gpu.amd.mi300x"

  validation {
    condition     = length(trimspace(var.instance_type)) > 0
    error_message = "instance_type cannot be empty."
  }
}
