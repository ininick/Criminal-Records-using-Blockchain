const CriminalRecord = artifacts.require("CriminalRecord");

module.exports = function (deployer) {
  deployer.deploy(CriminalRecord);
};
