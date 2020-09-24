# yazinc
Zinc zero-knowledge proofs on Yagna


## Project structure
* `requestor` contains files needed to run a requestor - this is what most people would need
* `provider` contains files needed to recreate image used by provider - you will only need them if you want to modify the way providers work

## Running

0. Install requirements: `pip install -r requestor/requirements.txt`
1. Install Zinc and execute preliminary steps as described in  https://zinc.matterlabs.dev/02-getting-started/01-first-circuit.html (the `zargo prove` step is optional as we will run it on Golem)

2. Assuming your yagna daemon is already running, run the requestor script  (mutatis mutandis)

```
python /path/to/yazinc/prove.py --circuit build/default.znb --proving-key data/proving-key --public-data data/public-data.json --witness data/witness.json
```

(NB the options are identical to these of `zvm prove`)

3. Verify the generated `proof.txt`:

```
zargo verify < proof.txt
```
