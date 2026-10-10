"""Tests for Response decorators, security headers, compression, and status lines."""

import zlib
import pytest
from pyresponse.response import (
    Attachment,
    BadRequest,
    Cached,
    Chunked,
    ContentType,
    Created,
    Etag,
    FrameOptions,
    Gzip,
    Header,
    Hsts,
    Inline,
    Location,
    NoSniff,
    NotFound,
    Ok,
    RetryAfter,
    Secure,
    ServerError,
    ServerTiming,
    Text,
    WithoutHeader,
)


@pytest.mark.asyncio
async def test_response_decorators():
    base = Ok(Text("content"))

    cached = Cached(base, max_age=120, directive="private")
    assert (await cached.head()).value("cache-control") == "private, max-age=120"

    etag = Etag(base, "abc123xyz")
    assert (await etag.head()).value("etag") == '"abc123xyz"'

    timing = ServerTiming(base, metric="query", dur=4.5)
    assert (await timing.head()).value("server-timing") == "query;dur=4.5"

    ct = ContentType(base, "application/xml")
    assert (await ct.head()).value("content-type") == "application/xml"


@pytest.mark.asyncio
async def test_response_statusline_and_header_decorators():
    base = Text("hello")
    assert (await Ok(base).head()).status() == 200
    assert (await Created(base).head()).status() == 201
    assert (await BadRequest(base).head()).status() == 400
    assert (await NotFound(base).head()).status() == 404
    assert (await ServerError(base).head()).status() == 500

    # Location decorator
    loc = Location(Ok(base), "https://example.com/redirect")
    assert (await loc.head()).value("location") == "https://example.com/redirect"

    # WithoutHeader decorator
    with_h = Header(Ok(base), "X-Remove-Me", "Temporary")
    assert (await with_h.head()).has("x-remove-me") is True
    without_h = WithoutHeader(with_h, "X-Remove-Me")
    assert (await without_h.head()).has("x-remove-me") is False

    # Attachment and Inline decorators
    att = Attachment(Ok(base), "report.pdf")
    assert (await att.head()).value("content-disposition") == 'attachment; filename="report.pdf"'

    inl = Inline(Ok(base), "preview.png")
    assert (await inl.head()).value("content-disposition") == 'inline; filename="preview.png"'


@pytest.mark.asyncio
async def test_response_stream_and_encoding_decorators():
    text_res = Ok(Text("The quick brown fox jumps over the lazy dog!"))

    # Gzip decorator
    gzipped = Gzip(text_res)
    head_gz = await gzipped.head()
    assert head_gz.value("content-encoding") == "gzip"
    assert head_gz.has("content-length") is False

    compressed_bytes = b"".join([c async for c in gzipped.body()])
    decompressed = zlib.decompress(compressed_bytes, 16 + zlib.MAX_WBITS)
    assert decompressed == b"The quick brown fox jumps over the lazy dog!"

    # Chunked decorator
    chunked = Chunked(text_res)
    head_chunked = await chunked.head()
    assert head_chunked.value("transfer-encoding") == "chunked"
    assert head_chunked.has("content-length") is False


@pytest.mark.asyncio
async def test_security_response_decorators():
    base = Ok(Text("secure content"))

    # NoSniff
    ns = NoSniff(base)
    assert (await ns.head()).value("x-content-type-options") == "nosniff"

    # FrameOptions
    fo = FrameOptions(base, "SAMEORIGIN")
    assert (await fo.head()).value("x-frame-options") == "SAMEORIGIN"

    # Hsts
    hsts = Hsts(base, max_age=600, include_subdomains=False)
    assert (await hsts.head()).value("strict-transport-security") == "max-age=600"

    # RetryAfter
    ra = RetryAfter(base, 120)
    assert (await ra.head()).value("retry-after") == "120"

    # Secure composite
    sec = Secure(base)
    head_sec = await sec.head()
    assert head_sec.value("x-content-type-options") == "nosniff"
    assert head_sec.value("x-frame-options") == "DENY"
    assert "strict-transport-security" in {k.decode("latin1").lower() for k, _ in head_sec.headers()}
