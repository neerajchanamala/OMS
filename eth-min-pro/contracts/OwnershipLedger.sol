// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract OwnershipLedger {
    struct Property {
        uint256 id;
        string location;
        uint256 price;
        address owner;
    }

    uint256 public propertyCount = 0;
    mapping(uint256 => Property) public properties;

    event PropertyRegistered(uint256 id, string location, uint256 price, address owner);
    event OwnershipTransferred(uint256 id, address newOwner);

    function registerProperty(string memory _location, uint256 _price) public {
        propertyCount++;
        properties[propertyCount] = Property(propertyCount, _location, _price, msg.sender);
        emit PropertyRegistered(propertyCount, _location, _price, msg.sender);
    }

    function transferOwnership(uint256 _propertyId, address _newOwner) public {
        require(properties[_propertyId].owner == msg.sender, "Not the owner");
        properties[_propertyId].owner = _newOwner;
        emit OwnershipTransferred(_propertyId, _newOwner);
    }

    function getProperty(uint256 _propertyId) public view returns (Property memory) {
        return properties[_propertyId];
    }
}
