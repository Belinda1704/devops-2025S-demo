terraform {
  cloud {
    organization = "ALU-Break-4"
    workspaces {
      name = "my-project-prod"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_kms_key" "ecr" {
  description             = "KMS key for encrypting ECR repositories"
  deletion_window_in_days = 7
}

resource "aws_ecr_repository" "app_repo" {
  name = "practice-app-repo"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "IMMUTABLE"

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr.arn
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}

