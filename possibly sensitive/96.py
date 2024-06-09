    "version" / Const(Int8ub, 0),
    "flags" / Const(Int24ub, 0),
    Padding(4, pattern=b"\x00"),
    "handler_type" / String(4),
    Padding(12, pattern=b"\x00"),  # Int32ub[3]
    "name" / CString(encoding="utf8")
)


VideoMediaHeaderBox = Struct(
    "type" / Const(b"vmhd"),
    "version" / Default(Int8ub, 0),
    "flags" / Const(Int24ub, 1),
    "graphics_mode" / Default(Int16ub, 0),
    "opcolor" / Struct(
        "red" / Default(Int16ub, 0),
        "green" / Default(Int16ub, 0),
        "blue" / Default(Int16ub, 0),
    ),
)

DataEntryUrlBox = PrefixedIncludingSize(Int32ub, Struct(
    "type" / Const(b"url "),
    "version" / Const(Int8ub, 0),
    "flags" / BitStruct(
        Padding(23), "self_contained" / Rebuild(Flag, ~this._.location)
    ),
    "location" / If(~this.flags.self_contained, CString(encoding="utf8")),
))

DataEntryUrnBox = PrefixedIncludingSize(Int32ub, Struct(
    "type" / Const(b"urn "),
    "version" / Const(Int8ub, 0),
    "flags" / BitStruct(
        Padding(23), "self_contained" / Rebuild(Flag, ~(this._.name & this._.location))
    ),
    "name" / If(this.flags == 0, CString(encoding="utf8")),
    "location" / If(this.flags == 0, CString(encoding="utf8")),
))

DataReferenceBox = Struct(
    "type" / Const(b"dref"),
    "version" / Const(Int8ub, 0),
    "flags" / Default(Int24ub, 0),
    "data_entries" / PrefixedArray(Int32ub, Select(DataEntryUrnBox, DataEntryUrlBox)),
)

# Sample Table boxes (stbl)

MP4ASampleEntryBox = Struct(
    "version" / Default(Int16ub, 0),
    "revision" / Const(Int16ub, 0),
    "vendor" / Const(Int32ub, 0),
    "channels" / Default(Int16ub, 2),
    "bits_per_sample" / Default(Int16ub, 16),
    "compression_id" / Default(Int16sb, 0),
    "packet_size" / Const(Int16ub, 0),
    "sampling_rate" / Int16ub,
    Padding(2)
)


class MaskedInteger(Adapter):
    def _decode(self, obj, context):
        return obj & 0x1F

    def _encode(self, obj, context):
        return obj & 0x1F


AAVC = Struct(
    "version" / Const(Int8ub, 1),
    "profile" / Int8ub,
    "compatibility" / Int8ub,
    "level" / Int8ub,
    EmbeddedBitStruct(
        Padding(6, pattern=b'\x01'),
        "nal_unit_length_field" / Default(BitsInteger(2), 3),
    ),
    "sps" / Default(PrefixedArray(MaskedInteger(Int8ub), PascalString(Int16ub)), []),
    "pps" / Default(PrefixedArray(Int8ub, PascalString(Int16ub)), [])
)

HVCC = Struct(
    EmbeddedBitStruct(
        "version" / Const(BitsInteger(8), 1),
        "profile_space" / BitsInteger(2),
        "general_tier_flag" / BitsInteger(1),
        "general_profile" / BitsInteger(5),
        "general_profile_compatibility_flags" / BitsInteger(32),
        "general_constraint_indicator_flags" / BitsInteger(48),
        "general_level" / BitsInteger(8),
        Padding(4, pattern=b'\xff'),
        "min_spatial_segmentation" / BitsInteger(12),
        Padding(6, pattern=b'\xff'),
        "parallelism_type" / BitsInteger(2),
        Padding(6, pattern=b'\xff'),
        "chroma_format" / BitsInteger(2),
        Padding(5, pattern=b'\xff'),