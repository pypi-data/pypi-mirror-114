name = "ec2-cluster"

from pathlib import Path
version_file = Path(__file__).parent/"VERSION"
__version__ = version_file.open('r').read().strip()

from ec2_cluster.instances.cluster import Cluster
from ec2_cluster.shells.control import ClusterShell
from ec2_cluster.config.config import ClusterConfig, ClusterConfigValidationError

