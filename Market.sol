pragma solidity ^0.8.0;

import "./FoxNFT.sol";
import "./FoxAccessControl.sol";


contract Marketplace {

    uint maxQuantity = 10;

    struct FoxProd {
        string name;
        string description;
        string uri;
        int quantity;
    }

    mapping (string => FoxProd) FoxProds;
    FoxNFT ft;
    FoxAccessControl public accessControls;
    
    constructor(FoxAccessControl _accessControls, FoxNFT _ft) {
        ft = _ft;
        accessControls = _accessControls;
        
    }
    
    function addMintRole() public {
        accessControls.addMinterRole(address(this));
    }
    
    add

    function buy(address to, string memory metadataURI ) public {
        // FoxNFT newFoxItem = new FoxNFT('FoxNFT', 'FOXNFT', 'https://ipfs.io/ipfs/QmPWVEUXjc7F77bhqPCkhuLgv9z44aR3fmeUkGxHTNHE1S' {from: creator});
        ft.mint(to, metadataURI);
    }
    
}