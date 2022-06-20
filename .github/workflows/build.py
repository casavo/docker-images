#!/usr/bin/env python3

import os
import yaml
import sys
import itertools
import subprocess

specs={}
repo = sys.argv[1] + "/" if len(sys.argv) > 1 else ""
modified_files = [ os.path.dirname(file) for file in sys.argv[2:] ]
for d in [ d for d in os.listdir(".") if not d.startswith(".") and os.path.isdir(d) and d in modified_files and os.path.isfile(os.path.join(d,"spec.yaml"))]:
    with open(os.path.join(d,"spec.yaml")) as f:
        specs[d]=yaml.safe_load(f)

for k, v in specs.items():
    platforms = v.get("platforms", ["linux/amd64"])

    for tags in [dict(zip(v["tags"].keys(), values)) for values in itertools.product(*v["tags"].values())]:
        postfix = "_".join([str(tags[ts_key]) for ts_key in sorted(tags.keys())])

        cmd = [
            "docker",
            "buildx",
            "build",
            "--push",
            "--platform",
            ','.join(platforms),
        ]

        for k2, v2 in tags.items():
            cmd.append("--build-arg")
            cmd.append(f"{k2}={v2}")

        cmd.append("-t")
        cmd.append(f"{repo}{v['image']}:{postfix}")
        cmd.append(k)

        print('========> ' + ' '.join(cmd))

        subprocess.check_call(cmd)
