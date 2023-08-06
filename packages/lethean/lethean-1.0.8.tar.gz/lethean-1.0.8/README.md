# lethean
Distributed Virtual Private Marketplace

## Requirements.

Python >= 3.6

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://gitlab.com/lthn.io/projects/sdk/clients/python.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://gitlab.com/lthn.io/projects/sdk/clients/python.git`)

Then import the package:
```python
import lethean
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import lethean
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import lethean
from pprint import pprint
from lethean.api import explorer_api
from lethean.model.block_dto import BlockDTO
from lethean.model.block_outputs_dto import BlockOutputsDTO
from lethean.model.emission_dto import EmissionDTO
from lethean.model.mempool_dto import MempoolDTO
from lethean.model.network_stats_dto import NetworkStatsDTO
from lethean.model.prove_transfer_dto import ProveTransferDTO
from lethean.model.raw_block_dto import RawBlockDTO
from lethean.model.raw_transaction_dto import RawTransactionDTO
from lethean.model.search_dto import SearchDTO
from lethean.model.transaction_dto import TransactionDTO
from lethean.model.transactions_dto import TransactionsDTO
from lethean.model.version_dto import VersionDTO
# Defining the host is optional and defaults to https://dvpm.io
# See configuration.py for a list of all supported configuration parameters.
configuration = lethean.Configuration(
    host = "https://dvpm.io"
)



# Enter a context with an instance of the API client
with lethean.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = explorer_api.ExplorerApi(api_client)
    id = "1008663" # str | Search id, must be block_number

    try:
        api_response = api_instance.get_block(id)
        pprint(api_response)
    except lethean.ApiException as e:
        print("Exception when calling ExplorerApi->get_block: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://dvpm.io*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ExplorerApi* | [**get_block**](docs/ExplorerApi.md#get_block) | **GET** /v1/explorer/chain/block/{id} | 
*ExplorerApi* | [**get_emission**](docs/ExplorerApi.md#get_emission) | **GET** /v1/explorer/chain/emission | 
*ExplorerApi* | [**get_mempool**](docs/ExplorerApi.md#get_mempool) | **GET** /v1/explorer/chain/mempool | 
*ExplorerApi* | [**get_network_info**](docs/ExplorerApi.md#get_network_info) | **GET** /v1/explorer/chain/stats | 
*ExplorerApi* | [**get_outputs_blocks**](docs/ExplorerApi.md#get_outputs_blocks) | **GET** /v1/explorer/chain/block/outputs | 
*ExplorerApi* | [**get_raw_block_data**](docs/ExplorerApi.md#get_raw_block_data) | **GET** /v1/explorer/chain/block/raw/{id} | 
*ExplorerApi* | [**get_raw_transaction_data**](docs/ExplorerApi.md#get_raw_transaction_data) | **GET** /v1/explorer/chain/transaction/raw/{tx_hash} | 
*ExplorerApi* | [**get_transaction**](docs/ExplorerApi.md#get_transaction) | **GET** /v1/explorer/chain/transaction/{tx_hash} | 
*ExplorerApi* | [**get_transactions**](docs/ExplorerApi.md#get_transactions) | **GET** /v1/explorer/chain/transactions | 
*ExplorerApi* | [**get_version**](docs/ExplorerApi.md#get_version) | **GET** /v1/explorer/chain/version | 
*ExplorerApi* | [**prove_transfer**](docs/ExplorerApi.md#prove_transfer) | **GET** /v1/explorer/validate/transfer | 
*ExplorerApi* | [**search_chain**](docs/ExplorerApi.md#search_chain) | **GET** /v1/explorer/chain/search/{id} | 


## Documentation For Models

 - [BlockDTO](docs/BlockDTO.md)
 - [BlockEntity](docs/BlockEntity.md)
 - [BlockOutputEntity](docs/BlockOutputEntity.md)
 - [BlockOutputsDTO](docs/BlockOutputsDTO.md)
 - [BlockOutputsEntity](docs/BlockOutputsEntity.md)
 - [EcdhInfo](docs/EcdhInfo.md)
 - [EmissionDTO](docs/EmissionDTO.md)
 - [EmissionEntity](docs/EmissionEntity.md)
 - [InputsEntity](docs/InputsEntity.md)
 - [MempoolDTO](docs/MempoolDTO.md)
 - [MempoolEntity](docs/MempoolEntity.md)
 - [MgsEntity](docs/MgsEntity.md)
 - [MixinEntity](docs/MixinEntity.md)
 - [NetworkStatsDTO](docs/NetworkStatsDTO.md)
 - [NetworkStatsEntity](docs/NetworkStatsEntity.md)
 - [OutputEntity](docs/OutputEntity.md)
 - [ProveTransferDTO](docs/ProveTransferDTO.md)
 - [ProveTransferEntity](docs/ProveTransferEntity.md)
 - [ProveTransferOutputsEntity](docs/ProveTransferOutputsEntity.md)
 - [RangeSigsEntity](docs/RangeSigsEntity.md)
 - [RawBlockDTO](docs/RawBlockDTO.md)
 - [RawBlockEntity](docs/RawBlockEntity.md)
 - [RawBlockMinerTx](docs/RawBlockMinerTx.md)
 - [RawBlockMinerVin](docs/RawBlockMinerVin.md)
 - [RawBlockMinerVinGen](docs/RawBlockMinerVinGen.md)
 - [RawBlockMinerVout](docs/RawBlockMinerVout.md)
 - [RawTransactionDTO](docs/RawTransactionDTO.md)
 - [RawTransactionEntity](docs/RawTransactionEntity.md)
 - [RawTransactionEntityVin](docs/RawTransactionEntityVin.md)
 - [RawTransactionEntityVinKey](docs/RawTransactionEntityVinKey.md)
 - [RawTransactionEntityVout](docs/RawTransactionEntityVout.md)
 - [RawTransactionEntityVoutTarget](docs/RawTransactionEntityVoutTarget.md)
 - [RawTransactionRctSignature](docs/RawTransactionRctSignature.md)
 - [RctSigEntity](docs/RctSigEntity.md)
 - [RctSigPrunable](docs/RctSigPrunable.md)
 - [SearchDTO](docs/SearchDTO.md)
 - [SearchEntity](docs/SearchEntity.md)
 - [TransactionBlock](docs/TransactionBlock.md)
 - [TransactionDTO](docs/TransactionDTO.md)
 - [TransactionEntity](docs/TransactionEntity.md)
 - [TransactionsDTO](docs/TransactionsDTO.md)
 - [TransactionsEntity](docs/TransactionsEntity.md)
 - [TxnEntity](docs/TxnEntity.md)
 - [VersionDTO](docs/VersionDTO.md)
 - [VersionEntity](docs/VersionEntity.md)
 - [VoutTarget](docs/VoutTarget.md)


## Documentation For Authorization

 All endpoints do not require authorization.

## Author

contact@lethean.io


## Notes for Large OpenAPI documents
If the OpenAPI document is large, imports in lethean.apis and lethean.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from lethean.api.default_api import DefaultApi`
- `from lethean.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:
```
import sys
sys.setrecursionlimit(1500)
import lethean
from lethean.apis import *
from lethean.models import *
```

