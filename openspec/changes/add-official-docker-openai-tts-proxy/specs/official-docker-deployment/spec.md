## ADDED Requirements

### Requirement: CPU-default official GPT-SoVITS deployment

The system SHALL provide a Docker Compose deployment that starts official GPT-SoVITS API on CPU by default without modifying official source files.

#### Scenario: Start CPU deployment

- **WHEN** the operator runs compose without profiles
- **THEN** the GPT-SoVITS API service starts with `device=cpu` and `is_half=false`
- **AND** official `api_v2.py` is used as the API entrypoint

### Requirement: GPU profile deployment

The system SHALL provide optional GPU-profile services for future CUDA hardware without affecting the default CPU deployment.

#### Scenario: Start GPU deployment

- **WHEN** the operator starts compose with the `gpu` profile on a CUDA-capable host
- **THEN** the GPU GPT-SoVITS API service starts with CUDA device settings from environment variables
- **AND** the CPU default service is not required for the GPU service to be defined

### Requirement: External persistence

The system SHALL keep models, reference audio, caches, outputs, and temporary data outside the repository through mounted persistence directories.

#### Scenario: Mount persistence root

- **WHEN** the GPT-SoVITS service starts
- **THEN** pretrained models, G2PW data, custom model weights, reference audio, cache, output, and temp paths are mounted from the configured data root

### Requirement: Repository template excludes machine paths

The repository Compose template SHALL NOT hard-code user-specific absolute paths such as `/stockroom/docker_container_data`.

#### Scenario: Inspect repository compose

- **WHEN** the repository compose template is viewed
- **THEN** it uses variables or relative defaults for host paths
- **AND** local absolute paths are only present in the machine-local runtime `.env` or compose copy outside the repository
