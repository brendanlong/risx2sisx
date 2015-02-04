# risx2sisx

Brendan Long <b.long@cablelabs.com>

This program splits MPEG-DASH "Representation Index Segments" into "Single Index Segments". It mainly exists for testing purposes, but is being made available in case it's useful for anyone else.

## Usage

Run `./risx2sisx.py -h` for usage information.

Simple example, split `representation.sidx` into `segment-1.sidx`, `segment-2.sidx`, etc. in the current directory:

    ./risx2sisx.py representation.sidx

More complicated example, split `uf3_iframe.sidx` into `segment-0001.sidx`, `segment-0002.sidx`, etc. in another directory:

    ./risx2sisx.py ~/Videos/dash/multi4_ssix_simple/uf3/uf3_iframe.sidx \
        -t '~/Videos/dash/multi4_ssix_simple/uf3/segment-{n:0>4}.sidx'

## Known Issues

  * Only a bare minimum of validation is done, so if your representation index is invalid, the output will likely be broken.
  * If you have more than one 'sidx' per segment, the splitting algorithm will be wrong. I'm not sure if this is allowed by the DASH spec, but I'm open to pull requests if you need support for this.
