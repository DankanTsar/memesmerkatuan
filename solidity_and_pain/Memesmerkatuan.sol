pragma solidity ^0.4.22;
pragma experimental ABIEncoderV2;

import "./Meme.sol";

contract Memesmerkatuan {
    string public constant name = "Memesmerkatuan";
    string public constant symbol = "MEM";
    uint8 public constant decimals = 18;
    uint public constant tenExpDecimals = 1000000000000000000;
    address owner;
    mapping(address=>uint256) amount;
    mapping(bytes32=>uint256) allow;
    address[] memes;
    uint256 totalSuppl;
    constructor (uint256 _totalSupply) public {
        owner = msg.sender;
        amount[owner] = _totalSupply;
        totalSuppl = _totalSupply;
    }
    function totalSupply() public view returns (uint256){
        return totalSuppl;
    }
    function balanceOf(address _owner) public view returns (uint256 balance){
        balance=amount[_owner];
    }
    function allowance(address _owner, address _spender) public view returns (uint256){
        bytes32 hsh = keccak256(_owner, _spender);
        return allow[hsh];
    }
    function transfer(address _to, uint256 _value) public returns (bool){
        if (amount[msg.sender] < _value){
            return false;
        }
        amount[msg.sender] -= _value;
        amount[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
    function approve(address _spender, uint256 _value) public returns (bool ){
        if (amount[msg.sender] < _value){
            return false;
        }
        bytes32 hsh = keccak256(msg.sender, _spender);
        allow[hsh] += _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool ){
        if(allowance(_from, _to) < _value){
            return false;
        }
        bytes32 hsh = keccak256(_from, _to);
        allow[hsh] -= _value;
        amount[_from] -= _value;
        amount[_to] += _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
    function addMeme(string meme_text) public {
        require(amount[msg.sender] > tenExpDecimals);
        amount[msg.sender] -= tenExpDecimals;
        Meme meme = new Meme(meme_text, msg.sender);
        memes.push(address(meme));
    }
    function getAllMemes() public view returns(address[]) {
        return memes;
    }
    function likeMeme(address meme) public {
        uint256 cost = 100000000000000000;
        require(amount[msg.sender] > cost);
        amount[msg.sender] -= cost;
        Meme obj_meme= Meme(meme);
        obj_meme.investMeme(msg.sender);
        uint256 creator_prize = cost / 2;
        cost -= creator_prize;
        amount[obj_meme.getOwner()] += creator_prize;
        address [] memory investors = obj_meme.getInvestors();
        uint256 investor_prize = cost / investors.length;
        for (uint32 i = 0; i < investors.length; ++i){
            amount[investors[i]] += investor_prize;
            cost -= investor_prize;
        }
        amount[owner] += cost;
    }
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}
