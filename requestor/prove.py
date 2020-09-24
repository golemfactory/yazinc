from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta

import argparse
import asyncio
import pathlib
import sys

async def main(circuit, proving_key, proving_tasks):
    package = await vm.repo(
        image_hash="c8a301a6cb1cb3a6fb2001d80493e5e8179a0283bd90d66f3dcac616",
        min_mem_gib=1.5,
        min_storage_gib=2.0,
    )

    async def worker(ctx: WorkContext, proving_tasks):
        ctx.send_file(circuit, "/golem/input/circuit.znb")
        ctx.send_file(proving_key, "/golem/input/proving-key")

        async for task in proving_tasks:
            data = task.data
            ctx.send_file(data["public"], "/golem/input/public-data.json")
            ctx.send_file(data["witness"], "/golem/input/witness.json")
            ctx.run("/golem/prove.sh")
            ctx.download_file(f"/golem/output/proof.txt", f"proof.txt")
            yield ctx.commit(task)
            # TODO: Check if job results are valid
            # and reject by: task.reject_task(msg = 'invalid file')
            task.accept_task()

        ctx.log("done")

    init_overhead: timedelta = timedelta(minutes=3)

    async with Engine(
        package=package,
        max_workers=3,
        budget=10.0,
        timeout=init_overhead + timedelta(minutes=len(proving_tasks) * 3),
        subnet_tag="testnet",
    ) as engine:

        async for progress in engine.map(
            worker, [Task(data=task) for task in proving_tasks]
        ):
            print("progress=", progress)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--circuit", required=True)
    ap.add_argument("--proving-key", required=True)
    ap.add_argument("--public-data", required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--output", required=True)
    arguments = ap.parse_args()
    circuit = arguments.circuit
    public_data = arguments.public_data
    witness = arguments.witness
    proving_key = arguments.proving_key
    proof = arguments.output
    print(f"circuit='{circuit}'")
    print(f"proving_key='{proving_key}'")
    #sys.exit(0)
    proving_tasks = [
        {"public": public_data, "witness": witness, "proof": proof}
    ]
    loop = asyncio.get_event_loop()
    task = loop.create_task(main(circuit, proving_key, proving_tasks))
    try:
        asyncio.get_event_loop().run_until_complete(task)
    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.3))
