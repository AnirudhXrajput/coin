// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CoinFlip {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function flip(bool _guess) public payable {
        require(msg.value > 0, "You need to bet some ether");
        bool result = (block.timestamp % 2 == 0);
        if (result == _guess) {
            payable(msg.sender).transfer(msg.value * 2);
        }
    }

    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }

    receive() external payable {}
}
