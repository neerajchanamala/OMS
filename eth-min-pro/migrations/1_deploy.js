const OwnershipLedger = artifacts.require("OwnershipLedger");

module.exports = function (deployer) {
  deployer.deploy(OwnershipLedger);
};
