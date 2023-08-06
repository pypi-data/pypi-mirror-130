from typing import Optional

from pydantic import BaseSettings


class NetworkStoreEnvironmentVariables(BaseSettings):
    class Config:
        env_file = "kisters_network_store.env"

    deployment_url: str
    mongodb_host: str
    enable_viewer: bool = True
    enable_access_control: bool = True
    mongodb_replica_set_name: Optional[str] = None  # Deprecated- use mongodb_host


settings = NetworkStoreEnvironmentVariables()
