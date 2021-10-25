// SPDX-License-Identifier:MIT

pragma solidity ^0.6.0; 

contract SimpleStorage{
    uint256 public favouriteNumber;
    
    struct Person{
        string name;
        uint256 favouriteNumber;
    }
    
    Person[] public people;
    
    mapping(string => uint256) public nameNumberMap;
    
    function store(uint256 _favouriteNumber) public{
        favouriteNumber=_favouriteNumber;
    }
    
    function addPerson(string memory _name,uint256 _favouriteNumber) public{
        people.push(Person({name:_name,favouriteNumber:_favouriteNumber}));
        nameNumberMap[_name] = _favouriteNumber;
    }
    
    function retrieve() public view returns(uint256){
        return favouriteNumber;
    }
    
}