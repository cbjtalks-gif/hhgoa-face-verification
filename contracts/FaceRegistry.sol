// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FaceRegistry {
    struct Record {
        bytes32 dataHash;
        string postUrl;
        uint256 timestamp;
        address verifiedBy;
        bool exists;
    }

    mapping(bytes32 => Record) private records;

    event FaceRecordRegistered(
        bytes32 indexed dataHash,
        string postUrl,
        uint256 timestamp,
        address indexed verifiedBy
    );

    function registerRecord(bytes32 _dataHash, string memory _postUrl) external {
        require(!records[_dataHash].exists, "Record already registered on-chain");

        records[_dataHash] = Record({
            dataHash: _dataHash,
            postUrl: _postUrl,
            timestamp: block.timestamp,
            verifiedBy: msg.sender,
            exists: true
        });

        emit FaceRecordRegistered(_dataHash, _postUrl, block.timestamp, msg.sender);
    }

    function verifyRecord(bytes32 _dataHash) external view returns (
        bool isValid,
        string memory postUrl,
        uint256 timestamp,
        address verifiedBy
    ) {
        Record memory rec = records[_dataHash];
        return (rec.exists, rec.postUrl, rec.timestamp, rec.verifiedBy);
    }
}