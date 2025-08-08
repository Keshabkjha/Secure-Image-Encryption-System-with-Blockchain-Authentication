<div align="center">
  <h1>Secure Image Encryption System with Blockchain Authentication</h1>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
  [![Hedera](https://img.shields.io/badge/Hedera-Hashgraph-000000)](https://hedera.com/)
  [![OpenCV](https://img.shields.io/badge/OpenCV-5.0.0-green)](https://opencv.org/)
  [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

  > **A Next-Generation Secure Image Encryption System with Blockchain-Based Authentication**
</div>

## 🌐 Overview

Secure Image Encryption System is a sophisticated solution for protecting digital images using advanced cryptographic techniques and blockchain technology. The system employs chaotic maps for encryption and leverages the Hedera Hashgraph blockchain for secure key management and authentication.

## ✨ Key Features

- **Advanced Encryption**: Utilizes Ikeda map and Circle map algorithms for secure image encryption
- **Blockchain Integration**: Leverages Hedera Hashgraph for secure key management and access control
- **Intelligent Region Selection**: YOLO-based object detection for selective encryption
- **Multi-Factor Authentication**: Combines password-based encryption with time-sensitive OTPs
- **Secure Key Management**: Implements secure key derivation and storage
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16.x or higher (for the blockchain component)
- Hedera Testnet account (for blockchain features)
- OpenCV and other dependencies (see requirements.txt)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Keshabkjha/Secure-Image-Encryption-System-with-Blockchain-Authentication.git
   cd Secure-Image-Encryption-System-with-Blockchain-Authentication
   ```

2. **Set up Python environment**:
   ```bash
   # Create and activate virtual environment (recommended)
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # OR
   source venv/bin/activate  # On macOS/Linux
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Set up Node.js backend**:
   ```bash
   cd Backend
   npm install
   ```

4. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update with your Hedera credentials and other settings

## 🛠 Project Structure

```
Secure-Image-Encryption-System-with-Blockchain-Authentication/
├── Backend/                  # Node.js backend (Express server)
│   └── server.js            # Main server file
├── secure_image_encryption/  # Core Python package
│   ├── core/                # Encryption/decryption logic
│   │   ├── chaotic_maps.py  # Chaotic map implementations
│   │   ├── encryption.py    # Encryption logic
│   │   └── decryption.py    # Decryption logic
│   └── utils/               # Utility functions
│       ├── file_ops.py      # File operations
│       └── security.py      # Security utilities
├── tests/                   # Test suite
├── .github/                 # GitHub configurations
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker configuration
└── README.md                # This file
```

## 🚀 Usage

### Starting the Application

1. **Start the backend server**:
   ```bash
   cd Backend
   node server.js
   ```
   The server will start on `http://localhost:3000`

2. **Access the application**:
   Open your browser and navigate to `http://localhost:3000`

### Basic Workflow

1. **Encryption**:
   - Upload your file through the interface
   - Select or create a visual pattern
   - Download the encrypted file and key

2. **Decryption**:
   - Upload the encrypted file and key
   - The system will use YOLO to verify the visual pattern
   - Download the decrypted file

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run Python tests
pytest tests/

# Generate coverage report
pytest --cov=src --cov-report=html
```

## 🐳 Docker Support

Run the application using Docker Compose:

```bash
docker-compose up --build
```

## 🏆 Advanced Features

### 🔒 Enhanced Security
- **Dual Chaotic Map Encryption**: Implements both Ikeda map (u=0.918) and Circle map (k=0.5) algorithms
- **Selective Region Encryption**: YOLO-based object detection for intelligent region selection
- **Blockchain-Enabled Key Management**: Secure key storage and verification on Hedera Hashgraph
- **Zero-Knowledge Proofs**: Implements zk-SNARKs for secure authentication without exposing sensitive data
- **Post-Quantum Cryptography**: Future-proof encryption resistant to quantum computing attacks

### 🛠 Technical Implementation
- **Multi-Layered Architecture**: Clear separation between encryption, blockchain, and UI layers
- **High Performance**: Optimized operations for time-critical cryptographic functions
- **Modular Design**: Extensible architecture for new encryption algorithms or blockchain networks
- **Containerized Deployment**: Docker support for consistent environments
- **Comprehensive Testing**: Extensive test coverage across all components

### 🌍 Real-World Applications
- **Healthcare**: Secure sharing of medical imaging with HIPAA compliance
- **Legal**: Tamper-evident document verification
- **Government**: Classified information protection
- **Financial**: Secure document exchange with audit trails
- **IoT**: Secure image transmission in IoT networks

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest features.

1. **Fork** the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Keshab Kumar Jha**  
Email: [keshabkumarjha876@gmail.com](mailto:keshabkumarjha876@gmail.com)  
LinkedIn: [Keshab Kumar Jha](https://www.linkedin.com/in/keshabkjha/)  
GitHub: [Keshabkjha](https://github.com/Keshabkjha)

Project Link: [https://github.com/Keshabkjha/Secure-Image-Encryption-System-with-Blockchain-Authentication](https://github.com/Keshabkjha/Secure-Image-Encryption-System-with-Blockchain-Authentication)

## 🙏 Acknowledgments

- Hedera Hashgraph team for their support and documentation
- OpenCV and YOLO communities
- All contributors who have helped improve this project
- All the open-source libraries that made this project possible
