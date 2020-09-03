resource "aws_cloudwatch_event_target" "CW-Target" {
  target_id = "CW-Alarm-Creation-RDS"
  rule      = aws_cloudwatch_event_rule.console.name
  arn       = aws_lambda_function.CW-Alarm-Creation-RDS.arn
}

resource "aws_cloudwatch_event_rule" "RDS-Alarm-Creation" {
  name        = "RDS-Alarm-Creation"
  description = "RDS-Alarm-Creation"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.rds"
  ],
  "detail-type": [
    "RDS DB Instance Event"
  ]
}
PATTERN
}
