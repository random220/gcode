# Google Cloud Utility Scripts

This directory contains a set of shell scripts located in the [gcloud](file:///home/om/x/gcloud/gcloud) subdirectory to simplify common Google Cloud Platform (GCP) operations, such as environment initialization, instance listing, creation, termination, and SSH access.

## Configuration

A shared configuration file, **[config.sh](file:///home/om/x/gcloud/gcloud/config.sh)**, defines common variables used across the utilities:

* `PROJECT`: GCP project ID (default: `myfree-501315`).
* `ZONE`: GCP compute engine zone (default: `us-central1-a`).
* `VM_NAME`: Compute engine virtual machine name (default: `vm1`).
* `MACHINE_TYPE`: GCE machine type (default: `e2-micro`).
* `IMAGE_FAMILY`: Image family for the OS (default: `debian-12`).
* `IMAGE_PROJECT`: Project supplying the OS image (default: `debian-cloud`).
* `TAGS`: Network tags applied to the instance (default: `ssh-server`).

---

## Utilities Overview

Here is a summary of the available utility scripts:

### 1. [ginit](file:///home/om/x/gcloud/gcloud/ginit)
* **Purpose**: Initializes the `gcloud` CLI environment and configures authentication.
* **Commands run**:
  - `gcloud init` for setting up account configuration and default settings.
  - `gcloud auth login --update-adc` to log in and update Application Default Credentials (ADC) for local development authentication.

### 2. [glist](file:///home/om/x/gcloud/gcloud/glist)
* **Purpose**: Lists GCP projects and details running Compute Engine instances.
* **Commands run**:
  - Lists projects to find active projects.
  - Automatically extracts the Project ID using `grep` and `awk` from the project list.
  - Runs `gcloud compute instances list` to show all virtual machines in the retrieved project.

### 3. [gmk](file:///home/om/x/gcloud/gcloud/gmk)
* **Purpose**: Creates a Google Compute Engine virtual machine instance using variables defined in `config.sh`.

### 4. [grm](file:///home/om/x/gcloud/gcloud/grm)
* **Purpose**: Deletes the VM instance specified in `config.sh`.

### 5. [gsh](file:///home/om/x/gcloud/gcloud/gsh)
* **Purpose**: Connects securely to the VM instance specified in `config.sh` via SSH.

---

## Usage

Before running any script, make sure to make them executable:
```bash
chmod +x gcloud/*.sh gcloud/g*
```
Then, you can execute them directly:

```bash
./gcloud/ginit
./gcloud/glist
./gcloud/gmk
./gcloud/gsh
./gcloud/grm
```
