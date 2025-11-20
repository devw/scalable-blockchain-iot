// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title IoTDataRegistry
 * @dev Lightweight smart contract for storing IoT sensor data using event-based logging
 * @notice This contract uses events instead of storage to minimize blockchain bloat
 */
contract IoTDataRegistry {
    
    // Event emitted when IoT data is received
    event IoTDataReceived(
        address indexed sender,
        string indexed sensorId,
        string data,
        uint256 timestamp,
        uint256 blockNumber
    );
    
    // Event emitted when a sensor is registered
    event SensorRegistered(
        address indexed owner,
        string indexed sensorId,
        string metadata,
        uint256 timestamp
    );
    
    // Counter for total data submissions
    uint256 public totalSubmissions;
    
    // Mapping to track if a sensor is registered (optional validation)
    mapping(string => bool) public registeredSensors;
    
    // Mapping to track sensor owners
    mapping(string => address) public sensorOwners;
    
    /**
     * @dev Register a new IoT sensor
     * @param sensorId Unique identifier for the sensor
     * @param metadata Additional sensor information (type, location, etc.)
     */
    function registerSensor(
        string memory sensorId,
        string memory metadata
    ) public {
        require(bytes(sensorId).length > 0, "Sensor ID cannot be empty");
        require(!registeredSensors[sensorId], "Sensor already registered");
        
        registeredSensors[sensorId] = true;
        sensorOwners[sensorId] = msg.sender;
        
        emit SensorRegistered(
            msg.sender,
            sensorId,
            metadata,
            block.timestamp
        );
    }
    
    /**
     * @dev Submit IoT sensor data to the blockchain
     * @param sensorId Unique identifier for the sensor
     * @param data Sensor data (can be JSON string, CSV, or any format)
     * @param timestamp Unix timestamp of when data was captured
     */
    function submitData(
        string memory sensorId,
        string memory data,
        uint256 timestamp
    ) public {
        require(bytes(sensorId).length > 0, "Sensor ID cannot be empty");
        require(bytes(data).length > 0, "Data cannot be empty");
        require(timestamp > 0, "Timestamp must be greater than 0");
        
        // Increment submission counter
        totalSubmissions++;
        
        // Emit event with data (stored in transaction logs)
        emit IoTDataReceived(
            msg.sender,
            sensorId,
            data,
            timestamp,
            block.number
        );
    }
    
    /**
     * @dev Batch submit multiple sensor readings
     * @param sensorIds Array of sensor identifiers
     * @param dataPoints Array of sensor data
     * @param timestamps Array of timestamps
     */
    function submitBatchData(
        string[] memory sensorIds,
        string[] memory dataPoints,
        uint256[] memory timestamps
    ) public {
        require(
            sensorIds.length == dataPoints.length && 
            dataPoints.length == timestamps.length,
            "Array lengths must match"
        );
        require(sensorIds.length > 0, "Cannot submit empty batch");
        require(sensorIds.length <= 50, "Batch size too large (max 50)");
        
        for (uint256 i = 0; i < sensorIds.length; i++) {
            submitData(sensorIds[i], dataPoints[i], timestamps[i]);
        }
    }
    
    /**
     * @dev Check if a sensor is registered
     * @param sensorId Sensor identifier to check
     * @return bool True if sensor is registered
     */
    function isSensorRegistered(string memory sensorId) public view returns (bool) {
        return registeredSensors[sensorId];
    }
    
    /**
     * @dev Get the owner of a registered sensor
     * @param sensorId Sensor identifier
     * @return address Owner address (0x0 if not registered)
     */
    function getSensorOwner(string memory sensorId) public view returns (address) {
        return sensorOwners[sensorId];
    }
    
    /**
     * @dev Get contract information
     * @return totalSubs Total number of data submissions
     * @return contractAddr Address of this contract
     */
    function getContractInfo() public view returns (
        uint256 totalSubs,
        address contractAddr
    ) {
        return (totalSubmissions, address(this));
    }
}