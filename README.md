# SecureCircle: YOLO-Enhanced Visual Encryption

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-16%2B-green.svg)](https://nodejs.org/)

SecureCircle is an innovative encryption solution that combines traditional cryptographic methods with YOLO (You Only Look Once) object detection to provide an additional layer of visual security. This project demonstrates how computer vision can enhance data protection through visual pattern recognition.

## ✨ Features

- 🔒 Dual-layer encryption combining traditional and visual cryptography
- 🎯 YOLO-based object detection for visual pattern recognition
- 🔄 Seamless integration between Python backend and Node.js server
- 📱 Responsive web interface for easy interaction
- 🔐 Secure key management and encryption protocols

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm (comes with Node.js)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/secure-circle.git
   cd secure-circle
   ```

2. **Set up Python environment**
   ```bash
   # Create and activate virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Configure backend**
   ```bash
   cd Backend
   npm install
   ```

4. **Environment Variables**
   Create a `.env` file in the Backend directory with the following variables:
   ```
   PORT=3000
   NODE_ENV=development
   ```

## 🛠 Usage

### Starting the Application

1. **Start the backend server**
   ```bash
   cd Backend
   node server.js
   ```
   The server will start on `http://localhost:3000`

2. **Access the web interface**
   Open your browser and navigate to `http://localhost:3000`

### Basic Workflow

1. **Encryption**
   - Upload your file through the web interface
   - Select or create a visual pattern
   - Download the encrypted file and key

2. **Decryption**
   - Upload the encrypted file and key
   - The system will use YOLO to verify the visual pattern
   - Download the decrypted file

## 📁 Project Structure

```
secure-circle/
├── Backend/                 # Node.js backend
│   ├── server.js            # Express server
│   ├── package.json         # Node.js dependencies
│   └── routes/              # API routes
├── python/                  # Core encryption/decryption
│   ├── encrypt.py           # Encryption module
│   ├── decrypt.py           # Decryption module
│   └── yolo11n-seg.pt       # YOLO model weights
├── static/                  # Frontend assets
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

[Your Name] - [your.email@example.com]

Project Link: [https://github.com/yourusername/secure-circle](https://github.com/yourusername/secure-circle)

## 🙏 Acknowledgments

- [YOLO](https://github.com/ultralytics/yolov5) for the object detection model
- [Node.js](https://nodejs.org/) and [Express](https://expressjs.com/)
- [OpenCV](https://opencv.org/) for computer vision capabilities
