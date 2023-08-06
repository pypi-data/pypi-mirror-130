# ⚡️📝 TLV Payment Metadata Records Parser for LND

Extract [custom TLV payment metadata records](https://klabo.blog/lightning/bitcoin/2021/03/21/custom-data-in-lightning-payments.html) that may have been attached to lightning payments you received.
For example, you can extract [boostagrams](https://twitter.com/HillebrandMax/status/1443519648125833218?s=20) from payments received through [value-for-value](https://podcastindex.org/podcast/value4value) podcasting [apps](https://podcastindex.org/apps).

For more information, see the [release notes of LND's v0.9 release](https://github.com/lightningnetwork/lnd/releases/tag/v0.9.0-beta).

## Installation

Make sure you have up-to-date installations of `pip` and `setuptools`:

```
pip install --upgrade pip
pip install --upgrade setuptools
```

Then install the `lntlvs` CLI:

```
pip install lntlvs
```

## Examples

By default, only podcast metadata will be extracted.
To query the first 100 payments on your node, run:

```
lntlvs --maxinvoices 100
```

To queriy from the next 100 payments, run:

```
lntlvs --maxinvoices 100 --indexoffset 100
```

To extract another type of custom records other than podcast metadata, specify the `--tlvkey` option.
To extract multiple types of custom records, repeat this option multiple times.
See [here](https://github.com/satoshisstream/satoshis.stream/blob/main/TLV_registry.md) for a list of TLV keys used in the open.

```
lntlvs --tlvkey 7629171 --tlvkey 7629169 # Extract tip note and podcast metadata
```

## Usage

```
Usage: lntlvs [OPTIONS]

  Extract custom metadata records that may have been attached to lightning payments you received.

Options:
  --tlscertpath <value>   Path to the TLS certificate for lnd's RPC service  [default: ~/.lnd/tls.cert]
  --macaroonpath <value>  Path to the (read-only) macaroon for lnd's RPC service  [default: ~/.lnd/data/chain/bitcoin/mainnet/readonly.macaroon]
  --rpchost <value>       The address and port where lnd's RPC service is listening  [default: 127.0.0.1:10009]
  --tlvkey <value>        A TLV key to extract - can be specified multiple times  [default: 7629169]
  --indexoffset <value>   Query for invoices starting at (not including) this offset  [default: 0]
  --maxinvoices <value>   The maximum number of invoices to query  [default: 1000]
  --help                  Show this message and exit.
```

## Development

Create a virtual environment:

```
python -m venv .venv && source .venv/bin/activate
```

Install production and development dependencies:

```
pip install -e ".[dev]"
```

### Re-generating gPRC Code

If required, update the LND interface definition in `src/protobuf/custom_records/generated/lightning.proto` by running:

```
src/protobuf/update.sh
```

Then re-generate the gPRC code with:

```
src/protobuf/generate.sh
```



