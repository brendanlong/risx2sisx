#!/usr/bin/env python3
import argparse
import itertools
import struct


class Box(object):
    def __init__(self, type, contents):
        self.type = type
        self.contents = contents

    def get_binary(self):
        size = 8 + len(self.contents)
        return struct.pack("!I4s", size, self.type) + self.contents

    @staticmethod
    def read(f):
        binary_size = f.read(4)
        if len(binary_size) != 4:
            return None
        size = struct.unpack("!I", binary_size)[0]
        data = f.read(size - 4)
        return Box(data[:4], data[4:])


class StypBox(object):
    def __init__(self, contents):
        self.major_brand = contents[:4]
        self.minor_version = struct.unpack("!I", contents[4:8])[0]
        self.compatible_brands = set(contents[i:i+4]
                                     for i in range(8, len(contents), 4))

    def get_binary(self):
        size = 16 + len(self.compatible_brands) * 4
        binary = struct.pack("!I4s4sI", size, b"styp", self.major_brand,
            self.minor_version)
        for brand in self.compatible_brands:
            binary += struct.pack("!4s", brand)
        return binary


def split_risx(risx_file_name, template):
    with open(risx_file_name, "rb") as f:
        box = Box.read(f)
        if box.type != b'styp':
            raise Exception("Representation Index starts with a {} box, but "
                "should start with an 'styp' box.".format(box.type))
        styp = StypBox(box.contents)
        if styp.major_brand == b"risx":
            styp.major_brand = b"sisx"
        styp.compatible_brands.discard(b"risx")
        styp.compatible_brands.add(b"sisx")

        first_sidx = Box.read(f)
        if first_sidx.type != b"sidx":
            raise Exception("Representation Index has a {} following 'styp', "
                "but should have an 'sidx'.".format(first_sidx.type))

        segment_number = 0
        segment_index = None
        for i in itertools.count():
            box = Box.read(f)
            if box is None:
                break
            if box.type == b"sidx":
                segment_number += 1
                print("Writing Segment Index #{}".format(segment_number))
                if segment_index is not None:
                    segment_index.close()
                segment_index = open(template.format(n=segment_number), "wb")
                segment_index.write(styp.get_binary())
            segment_index.write(box.get_binary())
        if segment_index is not None:
            segment_index.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("representation_index", help="The representation "
        "index to convert (generally a .sidx file).")
    parser.add_argument("--template", "-t", help="Template for segment index "
        "files. {n} will be replaced with the segment number (starting at 1).",
        default="segment-{n}.sidx")

    args = parser.parse_args()
    split_risx(args.representation_index, args.template)
