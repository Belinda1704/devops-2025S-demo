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

resource "aws_ecr_repository" "app_repo" {
  name = "practice-app-repo"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "IMMUTABLE"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.app_repo.repository_url
}

