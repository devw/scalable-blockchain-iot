# Scalable Blockchain IoT Framework

Lightweight blockchain platform designed for storing IoT sensor data and focused on addressing research challenges in decentralized systems performance.

## 🎯 Research Focus

This framework is purposed for in-depth analysis and experimentation in controlled environments (Docker/Kubernetes) to support scientific publication, focusing on:

* **Autoscaling and Performance:** Investigating autoscaling strategies within microservices and IoT data ingestion pipelines.
* **Blockchain Throughput:** Measuring and optimizing blockchain node throughput and transaction handling capabilities under high-load scenarios.
* **Traffic Spike Management:** Evaluating strategies for resilient traffic spike management in distributed, decentralized systems.
* **Controlled Environments:** Leveraging **Kubernetes** and **Docker** for creating reproducible, isolated clusters essential for scientific validation.
    

## 🏗️ Architecture Summary

The platform integrates a lightweight blockchain solution for data persistence with a scalable API layer.

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Blockchain Core** | Hardhat / Ganache | Smart Contract execution, ledger persistence (Ganache for production-like persistence). |
| **API Layer** | Node.js + Express + Ethers.js | Data ingestion, microservices integration, and transaction management. |
| **Smart Contracts** | Solidity | Secure, tamper-proof data storage logic. |

---

## 📚 Documentation & Operation

Detailed information for deployment, operation, and API reference has been moved to the documentation directory.

* **Architecture Details:** [ARCHITECTURE.MD](./docs/ARCHITECTURE.MD)
* **Quick Start & Setup:** [SERVICE_MANAGEMENT.MD](./docs/SERVICE_MANAGEMENT.MD) (Includes deployment and restart commands)
* **API Usage & Endpoints:** [API_USAGE.MD](./docs/API_USAGE.MD) / [API_REFERENCE.MD](./docs/API_REFERENCE.MD)
* **Troubleshooting Guide:** [TROUBLESHOOTING.MD](./docs/TROUBLESHOOTING.MD)

---

## 🔗 Project Context

This framework supports establishing and running Blockchain-IoT setups crucial for:
1.  **Data Analysis** for research publication.
2.  **Experimentation** with distributed system resilience and scalability.

---

## 📄 License

MIT