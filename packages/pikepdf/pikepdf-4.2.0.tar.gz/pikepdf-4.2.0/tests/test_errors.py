import pytest

import pikepdf
from pikepdf import Name, Pdf


@pytest.fixture
def vera(resources):
    # A file that is not linearized
    with Pdf.open(resources / 'veraPDF test suite 6-2-10-t02-pass-a.pdf') as pdf:
        yield pdf


def test_foreign_linearization(vera):
    assert not vera.is_linearized
    with pytest.raises(RuntimeError, match="not linearized"):
        vera.check_linearization()


@pytest.mark.parametrize('msg, expected', [('QPDF', 'pikepdf.Pdf')])
def test_translate_qpdf(msg, expected):
    assert pikepdf._qpdf._translate_qpdf(msg) == expected


@pytest.mark.parametrize('filter_', ['/ASCII85Decode', '/ASCIIHexDecode'])
def test_char_out_of_range(filter_):
    p = pikepdf.new()
    st = pikepdf.Stream(p, b'\xba\xad', Filter=Name(filter_))
    with pytest.raises(pikepdf.DataDecodingError):
        st.read_bytes()
