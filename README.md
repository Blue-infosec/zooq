zooq
====

Queue for MWZoo (and maybe other things too)

- Tasks discovered in ztasks/ subfolder
- Implement "zooq" class implementation, to be imported into other projects and extended
- Track tasks by creating unique id's of "taskname-objid" to track "task ids", utilize this to identify and de-dupe task submissions
- Support queue with low-pri FIFO insertion, and high-pri LIFO insertion characteristics
- Child tasks inherit insertion characteristics of parent task
- Don't support preemption
- Utilize fork-run-exit model (for now)

Setup
=====

You can manage multiple malware zoos with the same installation.

To set up a new, empty, malware zoo database + folder:

```bash
./make_zoo.sh new-folder
```


Running Daemon
==============

The software is expected to run as a persistent daemon. There are plenty of service wrappers to use out there, but the
basic method for running the tool from the command line is:

```bash
./start_zoo.sh new-folder
```

You would have to first use the command described above in the **Setup** section to create `new-folder` before running
this command to start the daemon. You can kill the daemon with CTRL-C on the terminal, or UNIX `kill` command when you
want to stop it.


Submit Sample
=============

Submitting a sample is also achieved via a helper script I've provided named `submit_new_file.py`. This script adds the
new sample into the folder structure, and then tells the daemon to kick off the analysis stages. You will need to provide
the location of the malware sample (which you may have in a temporary folder or something), as well as the location of the
malware zoo folder:

```bash
./submit_new_file.py -f file.exe -d event-20200625 -r new-folder
```

A new subdirectory named `event-20200625` will be created under the `new-folder` which is the new zoo you created in the
**Setup** step. A sub-sub-directory derived from the name `file.exe` will be created underneath that, and it will be a
folder that analysis results will be stored within, as well as the original file. Tracking metadata that connects this
file to the folder will be stored in `new-folder/zooqdb.sqlite`, and then the analysis steps will be run that are specified
in the `data` variable defined toward the bottom of `submit_new_file.py`. I have chosen to replace the periods in the
filename with underscores, when creating the sub-sub-directory name, in order to reduce ambiguity and make path traversal
easier for pattern matching.

So, this directory structure will be created:

```
new-folder/event-20200625/file_exe/
```

A copy of the file will be stored in it:

```
new-folder/event-20200625/file_exe/file.exe
```

Analyzers will be run, that will create more files. At the time of this writing, `exifdata` and `capa` analyzers were
built into the system. These generate the following two files:

```
new-folder/event-20200625/file_exe/exiftool.json
new-folder/event-20200625/file_exe/capa.json
```

These file names will be consistent across multiple files, helping facilitate discovery using UNIX tools like `find` or
path globbing such as:

```bash
for f in new-folder/*/*/capa.json; do
  jq '."meta"."timestamp"' $f
done
```

Extending with New Modules
==========================

Adding new modules can be done via a GitHub PR. A great template is [GitHub PR #1](https://github.com/ckane/zooq/pull/1),
where I added the `capa` analyzer. Make sure that `requirements.txt` is updated, as well as any data required at run-time
that isn't installed via `pip` is installed as (preferrably) a `git submodule` in this repo.
