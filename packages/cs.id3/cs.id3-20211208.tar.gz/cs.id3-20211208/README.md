Support for ID3 tags.
A cs.binary based parser/transcriber for ID3 tags
and a convenience wrapper for Doug Zongker's pyid3lib:
http://pyid3lib.sourceforge.net/

*Latest release 20211208*:
* ID3V1 and ID3V2 support.
* ID3V1Frame,ID3V2Frame: new .tagset() method to return a TagSet.
* ID3V1Frame.parse: trim trailing NULs from the comment field.
* Assorted other small changes.

## Class `EnhancedTagFrame(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An Enhanced Tag.

### Method `EnhancedTagFrame.parse(bfr)`

Parse an enhanced tag.

### Method `EnhancedTagFrame.transcribe(self)`

Transcribe the enhanced tag.

## Class `ID3(types.SimpleNamespace)`

Wrapper for pyid3lib.tag.

OBSOLETE.
Going away when I'm sure the other classes cover all this stuff off.

### Method `ID3.__getitem__(self, key)`

Fetch the text of the specified frame.

### Method `ID3.__setitem__(self, key, value)`

Set a frame text to `value`.

### Method `ID3.clean(self, attr)`

Strip NULs and leading and trailing whitespace.

### Method `ID3.flush(self, *a, **kw)`

Update the ID3 tags in the file if modified, otherwise no-op.
Clears the modified flag.

### Method `ID3.get_frame(self, frameid)`

Return the frame with the specified `frameid`, or None.

### Property `ID3.tag`

The tag mapping from `self.pathname`.

## Class `ID3V1Frame(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An ID3V1 or ID3v1.1 data frame as described in wikipedia:
https://en.wikipedia.org/wiki/ID3

The following fields are defined:
* `title`: up to 30 ASCII characters
* `artist`: up to 30 ASCII characters
* `album`: up to 30 ASCII characters
* `year`: 4 digit ASCII year
* `comment`: up to 30 ASCII bytes, NUL or whitespace padded,
  up to 28 ASCII bytes if `track` is nonzero
* `track`: 0 for no track, a number from 1 through 255 otherwise;
  if nonzero then the comment field may only be up to 28 bytes long
* `genre_id`: a number value from 0 to 255

### Method `ID3V1Frame.parse(bfr)`

Parse a 128 byte ID3V1 or ID3v1.1 record.

### Method `ID3V1Frame.tagset(self)`

Return a `TagSet` with the ID3 tag information.

### Method `ID3V1Frame.transcribe(self)`

Transcribe the ID3V1 frame.

## Class `ID3V22TagDataFrame(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An ID3 v2.2.0 tag data frame.

Reference doc: https://id3.org/id3v2-00

### Method `ID3V22TagDataFrame.tag_id_class(tag_id)`

Return the `AbstractBinary` subclass to decode the a tag body from its tag id.
Return `None` for unrecognised ids.

## Class `ID3V23TagDataFrame(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An ID3 v2.3.0 tag data frame.

Reference doc: https://id3.org/id3v2.3.0

### Method `ID3V23TagDataFrame.tag_id_class(tag_id)`

Return the `AbstractBinary` subclass to decode the a tag body from its tag id.
Return `None` for unrecognised ids.

## Class `ID3V2Frame(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An ID3v2 frame, based on the document at:
https://web.archive.org/web/20120527211939/http://www.unixgods.org/~tilo/ID3/docs/id3v2-00.html

### Method `ID3V2Frame.parse(bfr)`

Return an ID3v2 frame as described here:

### Method `ID3V2Frame.tagset(self)`

Return a `TagSet` with the ID3 tag information.

### Method `ID3V2Frame.transcribe(self)`

Transcribe the ID3v2 frame.

## Class `ID3V2Size(cs.binary.BinarySingleValue,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

An ID3v2 size field,
a big endian 4 byte field of 7-bit values, high bit 0.

### Method `ID3V2Size.parse_value(bfr)`

Read an ID3V2 size field from `bfr`, return the size.

### Method `ID3V2Size.transcribe_value(size)`

Transcribe a size in ID3v2 format.

## Class `ID3V2Tags(types.SimpleNamespace)`

An `ID3V2Tags` maps ID3V2 tag information as a `SimpleNamespace`.

### Method `ID3V2Tags.__getattr__(self, attr)`

Catch frame id attrs and their wordier versions.

### Method `ID3V2Tags.__setattr__(self, attr, value)`

Map attributes to frame ids, set the corresponding `__dict__` entry.

## Class `ISO8859_1NULString(cs.binary.BinarySingleValue,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

A NUL terminated string encoded with ISO8859-1.

### Method `ISO8859_1NULString.transcribe_value(s)`

pylint: disable=arguments-differ

## Function `padded_text(text, length, encoding='ascii')`

Encode `text` using `encoding`,
crop to a maximum of `length` bytes,
pad with NULs to `length` if necessary.

## Function `parse_padded_text(bfr, length, encoding='ascii')`

Fetch `length` bytes from `bfr`,
strip trailing NULs,
decode using `encoding` (default `'ascii'`),
strip trailling whitepsace.

## Class `TextEncodingClass(cs.binary.BinarySingleValue,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

A trite class to parse the single byte text encoding field.

## Class `TextInformationFrameBody(cs.binary.SimpleBinary,types.SimpleNamespace,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

A text information frame.

### Method `TextInformationFrameBody.parse(bfr)`

Parse the text from the frame.

### Method `TextInformationFrameBody.transcribe(self)`

Transcribe the frame.

## Class `UCS2NULString(cs.binary.BinarySingleValue,cs.binary.AbstractBinary,cs.binary.BinaryMixin)`

A NUL terminated string encoded with UCS-2.

We're cheating and using UTF16 for this.

### Method `UCS2NULString.transcribe_value(s)`

Transcribe text as UTF-16-LE with leading BOM and trailing NUL.

# Release Log



*Release 20211208*:
* ID3V1 and ID3V2 support.
* ID3V1Frame,ID3V2Frame: new .tagset() method to return a TagSet.
* ID3V1Frame.parse: trim trailing NULs from the comment field.
* Assorted other small changes.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20150116.2*:
pyid3lib not on PyPI, remove from requirements and mention in README

*Release 20150116*:
Initial PyPI release.
