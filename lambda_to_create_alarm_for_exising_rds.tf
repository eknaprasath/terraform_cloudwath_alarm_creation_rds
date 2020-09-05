resource "aws_lambda_function" "CW-Alarm-Creation-RDS-for-existing-instances" {
  description = "Lambda function to create cloudwatch alarms for RDS"
  filename      = "files/cloudwatch_rds.zip"
  function_name = var.lambda_name_rds_for_existing_rds_alarm
  role          = var.iam_role
  handler       = "cloudwatch_rds_for_existing.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = filebase64sha256("files/cloudwatch_rds_for_existing.zip")

  runtime = "python3.8"
  memory_size =  "128"
  timeout = "300"

  environment {
    variables = {
      sns_arn = var.sns_arn,
      cw_number_of_connections = var.cw_number_of_connections,
      cw_cpu_threshold = var.cw_cpu_threshold,
      cw_memory_threshold = var.cw_memory_threshold,
      cw_disk_threshold = var.cw_disk_threshold
    }
  }
}