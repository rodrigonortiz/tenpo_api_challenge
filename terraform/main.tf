terraform {
  required_version = ">= 0.14"

  required_providers {
    google = ">= 3.3"
  }
}

variable "gcr_path" {
  type        = string
  description = "Path grc"
}

variable "github_sha" {
  type        = string
  description = "Github sha"
}


provider "google" {
  project = "ID_PROYECTO_GCP" #indicar project id de gcp
}

# Activar Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"

  disable_on_destroy = true
}

# Crear Cloud Run service
resource "google_cloud_run_service" "run_service" {
  name     = "tenpo-api-backend-8"
  location = "us-central1"

  template {
    spec {
      containers {
        image = join(":", [var.gcr_path, var.github_sha])  
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }

  # # Espera que Cloud Run API este encendida
  depends_on = [google_project_service.run_api]
}

# Permite que usuarios sin autenticar puedan consultar el servicio
resource "google_cloud_run_service_iam_member" "run_all_users" {
  service  = google_cloud_run_service.run_service.name
  location = google_cloud_run_service.run_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Mostrar el service URL
output "service_url" {
  value = google_cloud_run_service.run_service.status[0].url
}