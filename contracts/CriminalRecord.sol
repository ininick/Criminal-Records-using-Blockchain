// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CriminalRecord {
    struct Record {
        string name;
        uint256 age;
        string city;
        string region;
        string crime;
        string punishment;
    }

    Record[] public records;
    address public owner;

    mapping(address => bool) public validators;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    modifier onlyValidator() {
        require(validators[msg.sender], "Only validators can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addValidator(address _validator) public onlyOwner {
        validators[_validator] = true;
    }

    function removeValidator(address _validator) public onlyOwner {
        validators[_validator] = false;
    }

    function addRecord(
        string memory _name,
        uint256 _age,
        string memory _city,
        string memory _region,
        string memory _crime,
        string memory _punishment
    ) public onlyValidator {
        records.push(Record(_name, _age, _city, _region, _crime, _punishment));
    }

    function updateRecord(
        uint256 _index,
        string memory _name,
        uint256 _age,
        string memory _city,
        string memory _region,
        string memory _crime,
        string memory _punishment
    ) public onlyValidator {
        require(_index < records.length, "Record does not exist");
        records[_index] = Record(_name, _age, _city, _region, _crime, _punishment);
    }

    function deleteRecord(uint256 _index) public onlyValidator {
        require(_index < records.length, "Record does not exist");
        
        // Shift all records one position to the left to fill the gap
        for (uint256 i = _index; i < records.length - 1; i++) {
            records[i] = records[i + 1];
        }
        records.pop(); // Remove the last element
    }

    function getRecords() public view returns (Record[] memory) {
        return records;
    }
}
