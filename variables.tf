variable "iam_role" {
  type        = string
  # default     = "arn:aws:iam::356143132518:role/lambda_iam_role"
  description = "Lambda IAM Role"
}
variable "lambda_name_rds" {
  type        = string
  default     = "CW-Alarm-Creation-RDS
  description = "lamda function name"
}
variable "sns_arn" {
  type        = string
  # default     = "arn:aws:sns:us-east-1:356143132518:cloudwatch_alarm"
  description = "SNS ARN which will be used to trigger notification by CloudWatch"
}
variable "cw_cpu_threshold" {
  type        = number
  default     = "80"
  description = "Threshold for CPU Utilization"
}
variable "cw_number_of_connections" {
  type        = number
  default     = "30"
  description = "Number of Database connection established"
}
variable "AWS_ACCESS_KEY" {
  type        = string
  description = "Access Key"
}
variable "SECRET_ACCESS_KEY" {
  type        = string
  description = "Secret Access Key"
}