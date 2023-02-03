variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "cluster_name" {
    description = "AWS EKS Cluster name"
    type        = string
    default     = "rozsar-eks-cluster"
}

variable "node_group_name" {
    description = "AWS Node Group"
    type        = string
    default     = "rozsar-ng"
}

variable "app_port" {
  type        = string
  default     = "32000"
  description = "port bound to app"
}
