from enum import Enum
from typing import Literal


class ProviderVendor(str, Enum):
    IBMQ = "IBMQ"
    AZURE_QUANTUM = "Azure Quantum"
    AWS_BRAKET = "AWS Braket"
    IONQ = "IonQ"


class ProviderTypeVendor:
    IBMQ = Literal[ProviderVendor.IBMQ]
    AZURE_QUANTUM = Literal[ProviderVendor.AZURE_QUANTUM]
    AWS_BRAKET = Literal[ProviderVendor.AWS_BRAKET]
    IONQ = Literal[ProviderVendor.IONQ]


class IonqBackendNames(str, Enum):
    SIMULATOR = "simulator"
    QPU = "qpu"


class AzureQuantumBackendNames(str, Enum):
    IONQ_SIMULATOR = "ionq.simulator"
    IONQ_QPU = "ionq.qpu"
    HONEYWELL_API_VALIDATOR1 = "honeywell.hqs-lt-s1-apival"
    HONEYWELL_API_VALIDATOR2 = "honeywell.hqs-lt-s2-apival"
    HONEYWELL_SIMULATOR1 = "honeywell.hqs-lt-s1-sim"
    HONEYWELL_SIMULATOR2 = "honeywell.hqs-lt-s2-sim"
    HONEYWELL_QPU1 = "honeywell.hqs-lt-s1"
    HONEYWELL_QPU2 = "honeywell.hqs-lt-s2"


class AWSBackendNames(str, Enum):
    AWS_BRAKET_SV1 = "SV1"
    AWS_BRAKET_TN1 = "TN1"
    AWS_BRAKET_DM1 = "dm1"
    AWS_BRAKET_ASPEN_9 = "Aspen-9"
    AWS_BRAKET_ASPEN_10 = "Aspen-10"
    AWS_BRAKET_IONQ = "IonQ Device"


class IBMQBackendNames(str, Enum):
    IBMQ_AER_SIMULATOR = "aer_simulator"
    IBMQ_AER_SIMULATOR_STATEVECTOR = "aer_simulator_statevector"
    IBMQ_AER_SIMULATOR_DENSITY_MATRIX = "aer_simulator_density_matrix"
    IBMQ_AER_SIMULATOR_MATRIX_PRODUCT_STATE = "aer_simulator_matrix_product_state"


class BackendNameLiteralsVendor:
    IONQ = Literal[IonqBackendNames.SIMULATOR, IonqBackendNames.QPU]
    AZURE_QUANTUM = Literal[
        AzureQuantumBackendNames.IONQ_SIMULATOR,
        AzureQuantumBackendNames.IONQ_QPU,
        AzureQuantumBackendNames.HONEYWELL_API_VALIDATOR1,
        AzureQuantumBackendNames.HONEYWELL_API_VALIDATOR2,
        AzureQuantumBackendNames.HONEYWELL_SIMULATOR1,
        AzureQuantumBackendNames.HONEYWELL_SIMULATOR2,
        AzureQuantumBackendNames.HONEYWELL_QPU1,
        AzureQuantumBackendNames.HONEYWELL_QPU2,
    ]
    AWS_BRAKET = Literal[
        AWSBackendNames.AWS_BRAKET_SV1,
        AWSBackendNames.AWS_BRAKET_TN1,
        AWSBackendNames.AWS_BRAKET_DM1,
        AWSBackendNames.AWS_BRAKET_ASPEN_9,
        AWSBackendNames.AWS_BRAKET_ASPEN_10,
        AWSBackendNames.AWS_BRAKET_IONQ,
    ]
    IBMQ = Literal[
        IBMQBackendNames.IBMQ_AER_SIMULATOR,
        IBMQBackendNames.IBMQ_AER_SIMULATOR_STATEVECTOR,
        IBMQBackendNames.IBMQ_AER_SIMULATOR_DENSITY_MATRIX,
        IBMQBackendNames.IBMQ_AER_SIMULATOR_MATRIX_PRODUCT_STATE,
    ]
