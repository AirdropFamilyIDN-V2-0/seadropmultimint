from web3 import Web3, HTTPProvider
from web3 import __version__ as web3_version
from packaging.version import Version
from eth_account import Account
from web3._utils.events import get_event_data
import time, sys, json

# Require Web3.py >= 7.12.0
REQUIRED_WEB3 = Version("7.12.0")
CURRENT_WEB3 = Version(web3_version)

if CURRENT_WEB3 != REQUIRED_WEB3:
    print(f"ERROR: Web3.py version {CURRENT_WEB3} is too old.")
    print(f"Please change/upgrade to Web3.py >= {REQUIRED_WEB3}")
    print("Run: pip uninstall web3")
    print("Run: pip install web3==7.12.0")
    sys.exit(1)

print(f"Web3.py version OK: {CURRENT_WEB3}")

# Constants
SEA_DROP_ADDR = "0x00005EA00Ac477B1030CE78506496e8C2dE24bf5"
MULTIMINT_ADDR = "0x0000436623460303688165dF6a00466B507d0259"

SUPPORTED_CHAIN_IDS = {1, 10, 42161, 8453, 143, 137, 2741, 43114, 80094, 999}

SEA_ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"CreatorPayoutAddressCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"DuplicateFeeRecipient","type":"error"},{"inputs":[],"name":"DuplicatePayer","type":"error"},{"inputs":[],"name":"FeeRecipientCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"FeeRecipientNotAllowed","type":"error"},{"inputs":[],"name":"FeeRecipientNotPresent","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"want","type":"uint256"}],"name":"IncorrectPayment","type":"error"},{"inputs":[{"internalType":"uint256","name":"feeBps","type":"uint256"}],"name":"InvalidFeeBps","type":"error"},{"inputs":[],"name":"InvalidProof","type":"error"},{"inputs":[{"internalType":"address","name":"recoveredSigner","type":"address"}],"name":"InvalidSignature","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"maximum","type":"uint256"}],"name":"InvalidSignedEndTime","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"minimumOrMaximum","type":"uint256"}],"name":"InvalidSignedFeeBps","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"maximum","type":"uint256"}],"name":"InvalidSignedMaxTokenSupplyForStage","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"maximum","type":"uint256"}],"name":"InvalidSignedMaxTotalMintableByWallet","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"minimum","type":"uint256"}],"name":"InvalidSignedMintPrice","type":"error"},{"inputs":[{"internalType":"uint256","name":"got","type":"uint256"},{"internalType":"uint256","name":"minimum","type":"uint256"}],"name":"InvalidSignedStartTime","type":"error"},{"inputs":[],"name":"MintQuantityCannotBeZero","type":"error"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"uint256","name":"allowed","type":"uint256"}],"name":"MintQuantityExceedsMaxMintedPerWallet","type":"error"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"}],"name":"MintQuantityExceedsMaxSupply","type":"error"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"uint256","name":"maxTokenSupplyForStage","type":"uint256"}],"name":"MintQuantityExceedsMaxTokenSupplyForStage","type":"error"},{"inputs":[{"internalType":"uint256","name":"currentTimestamp","type":"uint256"},{"internalType":"uint256","name":"startTimestamp","type":"uint256"},{"internalType":"uint256","name":"endTimestamp","type":"uint256"}],"name":"NotActive","type":"error"},{"inputs":[{"internalType":"address","name":"sender","type":"address"}],"name":"OnlyINonFungibleSeaDropToken","type":"error"},{"inputs":[],"name":"PayerCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"PayerNotAllowed","type":"error"},{"inputs":[],"name":"PayerNotPresent","type":"error"},{"inputs":[],"name":"SignatureAlreadyUsed","type":"error"},{"inputs":[],"name":"SignedMintsMustRestrictFeeRecipients","type":"error"},{"inputs":[],"name":"SignerCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"SignerNotPresent","type":"error"},{"inputs":[],"name":"TokenGatedDropAllowedNftTokenCannotBeDropToken","type":"error"},{"inputs":[],"name":"TokenGatedDropAllowedNftTokenCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"TokenGatedDropStageNotPresent","type":"error"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"},{"internalType":"uint256","name":"allowedNftTokenId","type":"uint256"}],"name":"TokenGatedNotTokenOwner","type":"error"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"},{"internalType":"uint256","name":"allowedNftTokenId","type":"uint256"}],"name":"TokenGatedTokenIdAlreadyRedeemed","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"bytes32","name":"previousMerkleRoot","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newMerkleRoot","type":"bytes32"},{"indexed":false,"internalType":"string[]","name":"publicKeyURI","type":"string[]"},{"indexed":false,"internalType":"string","name":"allowListURI","type":"string"}],"name":"AllowListUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"feeRecipient","type":"address"},{"indexed":true,"internalType":"bool","name":"allowed","type":"bool"}],"name":"AllowedFeeRecipientUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"newPayoutAddress","type":"address"}],"name":"CreatorPayoutAddressUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":false,"internalType":"string","name":"newDropURI","type":"string"}],"name":"DropURIUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"payer","type":"address"},{"indexed":true,"internalType":"bool","name":"allowed","type":"bool"}],"name":"PayerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"indexed":false,"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"}],"name":"PublicDropUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"minter","type":"address"},{"indexed":true,"internalType":"address","name":"feeRecipient","type":"address"},{"indexed":false,"internalType":"address","name":"payer","type":"address"},{"indexed":false,"internalType":"uint256","name":"quantityMinted","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"unitMintPrice","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"feeBps","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"dropStageIndex","type":"uint256"}],"name":"SeaDropMint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"signer","type":"address"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"indexed":false,"internalType":"struct SignedMintValidationParams","name":"signedMintValidationParams","type":"tuple"}],"name":"SignedMintValidationParamsUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"nftContract","type":"address"},{"indexed":true,"internalType":"address","name":"allowedNftToken","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"indexed":false,"internalType":"struct TokenGatedDropStage","name":"dropStage","type":"tuple"}],"name":"TokenGatedDropStageUpdated","type":"event"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getAllowListMerkleRoot","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getAllowedFeeRecipients","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"},{"internalType":"uint256","name":"allowedNftTokenId","type":"uint256"}],"name":"getAllowedNftTokenIdIsRedeemed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getCreatorPayoutAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"getFeeRecipientIsAllowed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"payer","type":"address"}],"name":"getPayerIsAllowed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getPayers","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getPublicDrop","outputs":[{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"signer","type":"address"}],"name":"getSignedMintValidationParams","outputs":[{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getSigners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getTokenGatedAllowedTokens","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"}],"name":"getTokenGatedDrop","outputs":[{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"address","name":"minterIfNotPayer","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"},{"components":[{"internalType":"uint256","name":"mintPrice","type":"uint256"},{"internalType":"uint256","name":"maxTotalMintableByWallet","type":"uint256"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"dropStageIndex","type":"uint256"},{"internalType":"uint256","name":"maxTokenSupplyForStage","type":"uint256"},{"internalType":"uint256","name":"feeBps","type":"uint256"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct MintParams","name":"mintParams","type":"tuple"},{"internalType":"bytes32[]","name":"proof","type":"bytes32[]"}],"name":"mintAllowList","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"address","name":"minterIfNotPayer","type":"address"},{"components":[{"internalType":"address","name":"allowedNftToken","type":"address"},{"internalType":"uint256[]","name":"allowedNftTokenIds","type":"uint256[]"}],"internalType":"struct TokenGatedMintParams","name":"mintParams","type":"tuple"}],"name":"mintAllowedTokenHolder","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"address","name":"minterIfNotPayer","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"mintPublic","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"nftContract","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"address","name":"minterIfNotPayer","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"},{"components":[{"internalType":"uint256","name":"mintPrice","type":"uint256"},{"internalType":"uint256","name":"maxTotalMintableByWallet","type":"uint256"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"dropStageIndex","type":"uint256"},{"internalType":"uint256","name":"maxTokenSupplyForStage","type":"uint256"},{"internalType":"uint256","name":"feeBps","type":"uint256"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct MintParams","name":"mintParams","type":"tuple"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"mintSigned","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"string[]","name":"publicKeyURIs","type":"string[]"},{"internalType":"string","name":"allowListURI","type":"string"}],"internalType":"struct AllowListData","name":"allowListData","type":"tuple"}],"name":"updateAllowList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updateAllowedFeeRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_payoutAddress","type":"address"}],"name":"updateCreatorPayoutAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"dropURI","type":"string"}],"name":"updateDropURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"payer","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updatePayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"}],"name":"updatePublicDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"signer","type":"address"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams","name":"signedMintValidationParams","type":"tuple"}],"name":"updateSignedMintValidationParams","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"allowedNftToken","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage","name":"dropStage","type":"tuple"}],"name":"updateTokenGatedDrop","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
MULTI_ABI = json.loads('[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"deployer","type":"address"},{"indexed":true,"internalType":"address","name":"nftAddress","type":"address"},{"indexed":false,"internalType":"address","name":"mintContract","type":"address"}],"name":"MintDeployed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"deployer","type":"address"},{"indexed":true,"internalType":"address","name":"nftAddress","type":"address"},{"indexed":false,"internalType":"address","name":"mintContract","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"MintWithdrawFailed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"deployer","type":"address"},{"indexed":true,"internalType":"address","name":"nftAddress","type":"address"},{"indexed":false,"internalType":"address","name":"mintContract","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"MintWithdrawSuccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"deployer","type":"address"},{"indexed":true,"internalType":"address","name":"nftAddress","type":"address"},{"indexed":false,"internalType":"uint256","name":"attempted","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"succeeded","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"failed","type":"uint256"}],"name":"MultiWithdrawSummary","type":"event"},{"inputs":[{"internalType":"address","name":"deployer","type":"address"},{"internalType":"address","name":"nftAddress","type":"address"}],"name":"getMintCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"deployer","type":"address"},{"internalType":"address","name":"nftAddress","type":"address"}],"name":"getMints","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"address","name":"nftaddress","type":"address"}],"name":"mintMulti","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"nftAddress","type":"address"},{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"withdrawAllForNft","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
ERC721_EVENTS_ABI = json.loads('[{"inputs":[],"name":"AlreadyInitialized","type":"error"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"CannotExceedMaxSupplyOfUint64","type":"error"},{"inputs":[{"internalType":"uint256","name":"basisPoints","type":"uint256"}],"name":"InvalidRoyaltyBasisPoints","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"}],"name":"MintQuantityExceedsMaxSupply","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"NewOwnerIsZeroAddress","type":"error"},{"inputs":[],"name":"NotNextOwner","type":"error"},{"inputs":[],"name":"OnlyAllowedSeaDrop","type":"error"},{"inputs":[],"name":"OnlyOwner","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"ProvenanceHashCannotBeSetAfterMintStarted","type":"error"},{"inputs":[],"name":"RoyaltyAddressCannotBeZeroAddress","type":"error"},{"inputs":[],"name":"SameTransferValidator","type":"error"},{"inputs":[],"name":"SignersMismatch","type":"error"},{"inputs":[],"name":"TokenGatedMismatch","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"}],"name":"AllowedSeaDropUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"newContractURI","type":"string"}],"name":"ContractURIUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"MaxSupplyUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newPotentialAdministrator","type":"address"}],"name":"PotentialOwnerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"previousHash","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"newHash","type":"bytes32"}],"name":"ProvenanceHashUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"receiver","type":"address"},{"indexed":false,"internalType":"uint256","name":"bps","type":"uint256"}],"name":"RoyaltyInfoUpdated","type":"event"},{"anonymous":false,"inputs":[],"name":"SeaDropTokenDeployed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"oldValidator","type":"address"},{"indexed":false,"internalType":"address","name":"newValidator","type":"address"}],"name":"TransferValidatorUpdated","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cancelOwnershipTransfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"contractURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"internalType":"uint256","name":"toTokenId","type":"uint256"}],"name":"emitBatchMetadataUpdate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"minter","type":"address"}],"name":"getMintStats","outputs":[{"internalType":"uint256","name":"minterNumMinted","type":"uint256"},{"internalType":"uint256","name":"currentTotalSupply","type":"uint256"},{"internalType":"uint256","name":"maxSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTransferValidationFunction","outputs":[{"internalType":"bytes4","name":"functionSignature","type":"bytes4"},{"internalType":"bool","name":"isViewFunction","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getTransferValidator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"__name","type":"string"},{"internalType":"string","name":"__symbol","type":"string"},{"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"},{"internalType":"address","name":"initialOwner","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"minter","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"mintSeaDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"maxSupply","type":"uint256"},{"internalType":"string","name":"baseURI","type":"string"},{"internalType":"string","name":"contractURI","type":"string"},{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"},{"internalType":"string","name":"dropURI","type":"string"},{"components":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"string[]","name":"publicKeyURIs","type":"string[]"},{"internalType":"string","name":"allowListURI","type":"string"}],"internalType":"struct AllowListData","name":"allowListData","type":"tuple"},{"internalType":"address","name":"creatorPayoutAddress","type":"address"},{"internalType":"bytes32","name":"provenanceHash","type":"bytes32"},{"internalType":"address[]","name":"allowedFeeRecipients","type":"address[]"},{"internalType":"address[]","name":"disallowedFeeRecipients","type":"address[]"},{"internalType":"address[]","name":"allowedPayers","type":"address[]"},{"internalType":"address[]","name":"disallowedPayers","type":"address[]"},{"internalType":"address[]","name":"tokenGatedAllowedNftTokens","type":"address[]"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage[]","name":"tokenGatedDropStages","type":"tuple[]"},{"internalType":"address[]","name":"disallowedTokenGatedAllowedNftTokens","type":"address[]"},{"internalType":"address[]","name":"signers","type":"address[]"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams[]","name":"signedMintValidationParams","type":"tuple[]"},{"internalType":"address[]","name":"disallowedSigners","type":"address[]"}],"internalType":"struct ERC721SeaDropStructsErrorsAndEvents.MultiConfigureStruct","name":"config","type":"tuple"}],"name":"multiConfigure","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"provenanceHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"royaltyAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"royaltyBasisPoints","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"_salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newBaseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"newContractURI","type":"string"}],"name":"setContractURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"newMaxSupply","type":"uint256"}],"name":"setMaxSupply","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"newProvenanceHash","type":"bytes32"}],"name":"setProvenanceHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"royaltyAddress","type":"address"},{"internalType":"uint96","name":"royaltyBps","type":"uint96"}],"internalType":"struct ISeaDropTokenContractMetadata.RoyaltyInfo","name":"newInfo","type":"tuple"}],"name":"setRoyaltyInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newValidator","type":"address"}],"name":"setTransferValidator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newPotentialOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"string[]","name":"publicKeyURIs","type":"string[]"},{"internalType":"string","name":"allowListURI","type":"string"}],"internalType":"struct AllowListData","name":"allowListData","type":"tuple"}],"name":"updateAllowList","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"feeRecipient","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updateAllowedFeeRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"allowedSeaDrop","type":"address[]"}],"name":"updateAllowedSeaDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"payoutAddress","type":"address"}],"name":"updateCreatorPayoutAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"string","name":"dropURI","type":"string"}],"name":"updateDropURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"payer","type":"address"},{"internalType":"bool","name":"allowed","type":"bool"}],"name":"updatePayer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"publicDrop","type":"tuple"}],"name":"updatePublicDrop","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"signer","type":"address"},{"components":[{"internalType":"uint80","name":"minMintPrice","type":"uint80"},{"internalType":"uint24","name":"maxMaxTotalMintableByWallet","type":"uint24"},{"internalType":"uint40","name":"minStartTime","type":"uint40"},{"internalType":"uint40","name":"maxEndTime","type":"uint40"},{"internalType":"uint40","name":"maxMaxTokenSupplyForStage","type":"uint40"},{"internalType":"uint16","name":"minFeeBps","type":"uint16"},{"internalType":"uint16","name":"maxFeeBps","type":"uint16"}],"internalType":"struct SignedMintValidationParams","name":"signedMintValidationParams","type":"tuple"}],"name":"updateSignedMintValidationParams","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"seaDropImpl","type":"address"},{"internalType":"address","name":"allowedNftToken","type":"address"},{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint8","name":"dropStageIndex","type":"uint8"},{"internalType":"uint32","name":"maxTokenSupplyForStage","type":"uint32"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct TokenGatedDropStage","name":"dropStage","type":"tuple"}],"name":"updateTokenGatedDrop","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

# Symbol map for native token display
SYMBOLS = {
    1: "ETH",
    10: "ETH",
    42161: "ETH",
    8453: "ETH",
    137: "POL",
    43114: "AVAX",
    143: "MON",
    2741: "ETH",
    80094: "BERA",
    999: "HYPE"
}

# Helpers ---------------------------------------------------------------------

def to_checksum(addr: str) -> str:
    return Web3.to_checksum_address(addr)

def parse_gas_price_gwei_input(inp: str, w3: Web3) -> int:
    """
    Interpret input as GWEI decimal (e.g. '0.0001', '0.01', '1').
    If blank or only whitespace, use node gas price * 1.2.
    Returns gas price in wei (int).
    """
    try:
        if inp is None:
            base = w3.eth.gas_price
            return int(base * 1.2)
        s = inp.strip()
        if s == "":
            base = w3.eth.gas_price
            return int(base * 1.2)
        # allow user to specify "gwei" suffix optionally
        s_norm = s.lower().replace("gwei", "").strip()
        gwei_value = float(s_norm)
        wei = int(gwei_value * 1_000_000_000)
        return wei
    except Exception as e:
        print("Invalid gas price input; falling back to node gas price * 1.2. (e)", e)
        base = w3.eth.gas_price
        return int(base * 1.2)

def wei_to_native_str(wei: int) -> str:
    return f"{wei / 1e18:.18g}"

def gwei_from_wei(wei: int) -> float:
    return wei / 1e9

# Parse mint receipt: collect child mint addresses and tokenIds minted to them
def parse_mint_receipt(w3: Web3, receipt, multimint_addr_checksum):
    """
    Robust parse of a mint receipt:
      - finds MintDeployed events emitted by MULTIMINT_ADDR
      - collects child mint contract addresses and nftAddress (first occurrence)
      - decodes Transfer events in the receipt and collects tokenIds that were sent to those child addresses
    Returns: (nftAddress_or_None, list_of_child_mint_addrs, list_of_tokenIds)
    """
    try:
        # create lightweight event-only contracts to get event ABIs
        mm_contract = w3.eth.contract(abi=MULTI_ABI)            # has MintDeployed event ABI
        transfer_contract = w3.eth.contract(abi=ERC721_EVENTS_ABI) # has Transfer event ABI

        # get canonical event abi objects
        mint_ev_abi = mm_contract.events.MintDeployed._get_event_abi()
        transfer_ev_abi = transfer_contract.events.Transfer._get_event_abi()

        child_addrs = []
        nft_addr = None

        # First pass: find MintDeployed logs emitted by the multiMint contract
        for log in receipt.logs:
            # ensure addresses are comparable
            try:
                log_addr = Web3.to_checksum_address(log.address)
            except Exception:
                # if log doesn't have address field skip
                continue

            if log_addr.lower() != multimint_addr_checksum.lower():
                continue

            # decode using get_event_data
            try:
                ev = get_event_data(w3.codec, mint_ev_abi, log)
                args = ev["args"]
                # note: args keys are 'deployer','nftAddress','mintContract' per your event ABI
                if "mintContract" in args:
                    child_addrs.append(Web3.to_checksum_address(args["mintContract"]))
                if nft_addr is None and "nftAddress" in args:
                    nft_addr = Web3.to_checksum_address(args["nftAddress"])
            except Exception:
                # not decodable as MintDeployed or malformed - skip
                continue

        # If no child mints found, still try to decode Transfers (maybe tokens minted elsewhere)
        token_ids = []
        if child_addrs:
            child_set = {a.lower() for a in child_addrs}

            # Second pass: decode Transfer logs and collect tokenIds sent to child addresses
            for log in receipt.logs:
                try:
                    ev = get_event_data(w3.codec, transfer_ev_abi, log)
                    to_addr = Web3.to_checksum_address(ev["args"]["to"])
                    token_id = ev["args"]["tokenId"]
                    if to_addr.lower() in child_set:
                        # ensure int
                        token_ids.append(int(token_id))
                except Exception:
                    # not a Transfer log or failed decode
                    continue

        return nft_addr, child_addrs, token_ids

    except Exception as e:
        # bubble up the error (caller expected exceptions as 'e')
        raise

# Sign, send and wait helper (simple wrapper)
def sign_send_wait(w3: Web3, acct: Account, tx: dict, timeout=600):
    """
    Sign transaction dict with acct and send; wait for receipt.
    Returns receipt.
    """
    try:
        # Ensure nonce and chainId filled
        if "nonce" not in tx:
            tx["nonce"] = w3.eth.get_transaction_count(acct.address)
        if "chainId" not in tx:
            tx["chainId"] = w3.eth.chain_id

        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print("Sent Tx : ", tx_hash.hex())
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        return receipt
    except Exception as e:
        raise

# MAIN -----------------------------------------------------------------------
print(f'Auto SeaDrop MultiMint By ADFMIDN Team')
print(f'')
def main():
    try:
        rpc = input("Input RPC URL : ").strip()
        if not rpc:
            print("RPC URL Required!")
            return
        w3 = Web3(HTTPProvider(rpc, request_kwargs={"timeout": 60}))
        connected = w3.is_connected()
        print("Connected :", connected)
        if not connected:
            print("Unable To Connect To RPC. Exiting...")
            return

        chain_id = w3.eth.chain_id
        print("chainId =", chain_id)
        if chain_id not in SUPPORTED_CHAIN_IDS:
            print("Chain Not Supported. Supported : ", SUPPORTED_CHAIN_IDS)
            return
        native_symbol = SYMBOLS.get(chain_id, "ETH")

        # Contracts
        sea_drop = to_checksum(SEA_DROP_ADDR)
        multimint = to_checksum(MULTIMINT_ADDR)
        sea_contract = w3.eth.contract(address=sea_drop, abi=SEA_ABI)
        multi_contract = w3.eth.contract(address=multimint, abi=MULTI_ABI)

        # Wallet
        pk = input("Input Private Key EVM : ").strip()
        acct = Account.from_key(pk)
        print("Using Address : ", acct.address)

        # Gas price input (GWEI decimal) - blank -> node gas * 1.2
        gas_inp = input("Input Custom GWEI/Gas Price ( 0.01/1/10/100 ) Or Leave Blank [Default] : ")
        gas_price = parse_gas_price_gwei_input(gas_inp, w3)
        print(f"Using Gas Price : {gwei_from_wei(gas_price)}")

        # Menu
        print("\nMenu :\n1.) Mint Loop & Withdraw\n2.) Mint Loop Only\n3.) Withdraw Only")
        choice = input("Choose (1/2/3) : ").strip()

        if choice in ("1", "2"):
            nft_raw = input("NFT Contract Address : ").strip()
            nft_addr = to_checksum(nft_raw)
            total = int(input("Total Mint NFT : ").strip())

            # read price
            try:
                tup = sea_contract.functions.getPublicDrop(nft_addr).call()
                price = int(tup[0])
            except Exception as e:
                print("Failed Read Price From SeaDrop : ", e)
                return

            required_total_cost = price * total
            price_native = float(price) / 1e18
            total_native = float(required_total_cost) / 1e18
            print(f"Price Per Token : {price_native:g} {native_symbol}")
            print(f"Total Cost For {total} : {total_native:g} {native_symbol}")

            bal = w3.eth.get_balance(acct.address)
            bal_native = float(bal) / 1e18
            print(f"Wallet Native Balance: {bal_native:g} {native_symbol}")
            if bal < required_total_cost:
                print("Not Enought Native Balance! Exiting...")
                return

            attempt = 0
            while True:
                attempt += 1
                try:
                    print(f"Attempt #{attempt}: Building Mint TX...")
                    value = required_total_cost
                    nonce = w3.eth.get_transaction_count(acct.address)
                    func = multi_contract.functions.mintMulti(total, nft_addr)

                    # estimate gas: if this fails, error out (no fallback)
                    estimated_gas = func.estimate_gas({"from": acct.address, "value": value})
                    print("Estimated Gas : ", estimated_gas)

                    tx = func.build_transaction({
                        "chainId": chain_id,
                        "from": acct.address,
                        "value": value,
                        "gas": int(estimated_gas * 1.2),
                        "gasPrice": gas_price,
                        "nonce": nonce
                    })

                    # sign & send, wait for receipt
                    receipt = sign_send_wait(w3, acct, tx)
                    print("Mint Receipt Status : ", receipt.status)
                    if receipt.status == 1:
                        print("Mint TX Succeeded : ", receipt.transactionHash.hex())
                        if choice == "1":
                            try:
                                nft_detected, child_addrs, token_ids = parse_mint_receipt(w3, receipt, multimint)
                            except Exception as e:
                                print("Failed To Parse Logs From Mint Transaction Hash : ", e)
                                return

                            if nft_detected is None:
                                print("Could Not Detect NFT Address From Logs, Aborting Withdraw.")
                                return

                            print("Detected NFT Address : ", nft_detected)
                            print("Detected Token IDs : ", token_ids)

                            # withdraw
                            try:
                                withdraw_func = multi_contract.functions.withdrawAllForNft(nft_detected, token_ids)
                                nonce2 = w3.eth.get_transaction_count(acct.address)
                                est_gas_withdraw = withdraw_func.estimate_gas({"from": acct.address})
                                print("Withdraw Estimated Gas : ", est_gas_withdraw)
                                tx_w = withdraw_func.build_transaction({
                                    "chainId": chain_id,
                                    "from": acct.address,
                                    "gas": int(est_gas_withdraw * 1.2),
                                    "gasPrice": gas_price,
                                    "nonce": nonce2,
                                })
                                rcpt_w = sign_send_wait(w3, acct, tx_w)
                                print("Withdraw Receipt Status : ", rcpt_w.status)
                                if rcpt_w.status == 1:
                                    print("Withdraw Succeeded : ", rcpt_w.transactionHash.hex())
                                else:
                                    print("Withdraw Failed : ", rcpt_w.transactionHash.hex())
                            except Exception as e:
                                print("Withdraw Step Failed : ", e)
                        break
                    else:
                        print("Mint TX Failed Retrying...")
                        # time.sleep(3)
                        continue

                except Exception as e:
                    # surface estimate_gas errors and any other errors
                    print("Mint Attempt Exception : ", e)
                    print("Retrying...")
                    # time.sleep(3)
                    continue

        elif choice == "3":
            tx_hash_input = input("Input Mint Transaction Hash (0x...): ").strip()
            if not tx_hash_input.startswith("0x"):
                print("Invalid Transaction Hash")
                return
            try:
                receipt = w3.eth.get_transaction_receipt(tx_hash_input)
            except Exception as e:
                print("Failed To Fetch Mint Transaction Hash : ", e)
                return
            try:
                nft_detected, child_addrs, token_ids = parse_mint_receipt(w3, receipt, multimint)
            except Exception as e:
                print("Failed To Parse Logs From Mint Transaction Hash", e)
                return
            if nft_detected is None:
                print("Could Not Detect NFT Address From Logs, Aborting Withdraw.")
                return
            print("Detected NFT Address : ", nft_detected)
            print("Detected Token IDs : ", token_ids)

            try:
                withdraw_func = multi_contract.functions.withdrawAllForNft(nft_detected, token_ids)
                nonce2 = w3.eth.get_transaction_count(acct.address)
                est_gas_withdraw = withdraw_func.estimate_gas({"from": acct.address})
                print("Withdraw Estimated Gas : ", est_gas_withdraw)

                tx_w = withdraw_func.build_transaction({
                    "chainId": chain_id,
                    "from": acct.address,
                    "gas": int(est_gas_withdraw * 1.2),
                    "gasPrice": gas_price,
                    "nonce": nonce2,
                })
                rcpt_w = sign_send_wait(w3, acct, tx_w)
                print("Withdraw Receipt Status : ", rcpt_w.status)
                if rcpt_w.status == 1:
                    print("Withdraw Succeeded : ", rcpt_w.transactionHash.hex())
                else:
                    print("Withdraw Failed : ", rcpt_w.transactionHash.hex())
            except Exception as e:
                print("Withdraw Transaction Failed:", e)

        else:
            print("Invalid Choice. Exiting...")

    except Exception as e:
        print("Fatal Error : ", e)


if __name__ == "__main__":
    main()
