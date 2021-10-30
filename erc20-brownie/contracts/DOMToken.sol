// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DOMToken is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("DOMToken", "DOM") {
        _mint(msg.sender, initialSupply);
    }
}
