pragma solidity ^0.4.22;
pragma experimental ABIEncoderV2;

contract Meme{
    string str;
    address owner;
    address merkatuan;
    address[] investments;
    constructor(string _str, address _owner) public{
        merkatuan = msg.sender;
        owner = _owner;
        str = _str;
    }
    function getStr() public view returns(string) {
        return str;
    }
    function getOwner() public view returns(address) {
        return owner;
    }
    function investMeme(address investor){
        require(msg.sender == merkatuan);
        investments.push(investor);
    }
    function getInvestors() public view returns(address[]) {
        return investments;
    }
}