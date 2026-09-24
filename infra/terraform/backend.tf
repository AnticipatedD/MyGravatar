# Copyright Advanced Micro Devices, Inc.
#
# SPDX-License-Identifier: MIT

terraform {
  # Configures a secure, centralized state configuration repository
  backend "s3" {
    bucket         = "amd-mygravatar-terraform-state"
    key            = "infra/state/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "amd-mygravatar-state-locks"
    encrypt        = true
  }
}
