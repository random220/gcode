# GCloud Utilities

This directory contains shell script utilities for simplifying GCP operations.

## Configuration

* **[config.sh](file:///home/om/x/gcloud/gcloud/config.sh)**: A shared configuration file specifying settings like `PROJECT`, `ZONE`, `VM_NAME`, `MACHINE_TYPE`, etc.

## Scripts

* **[ginit](file:///home/om/x/gcloud/gcloud/ginit)**: Initializes the gcloud CLI (`gcloud init`) and logs in (`gcloud auth login --update-adc`).
* **[glist](file:///home/om/x/gcloud/gcloud/glist)**: Lists GCP projects and lists running compute instances in the active project.
* **[gmk](file:///home/om/x/gcloud/gcloud/gmk)**: Creates a GCE VM instance using parameters configured in `config.sh`.
* **[grm](file:///home/om/x/gcloud/gcloud/grm)**: Deletes the VM instance specified in `config.sh`.
* **[gsh](file:///home/om/x/gcloud/gcloud/gsh)**: Connects to the VM instance specified in `config.sh` via SSH.

## Usage
Ensure files are executable:

```bash
chmod +x *.sh g*
```

And execute them:

```bash
./ginit
```
