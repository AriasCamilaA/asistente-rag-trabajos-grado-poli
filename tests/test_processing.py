import pytest
from src.rag import chunks, normalize

def test_chunking_covers_tail_without_loss():
    words=[str(i) for i in range(403)]
    result=list(chunks(' '.join(words)))
    assert result[-1].split()[-1]=='402'
    assert all(len(x.split())<=180 for x in result)
    assert result[0].split()[-30:]==result[1].split()[:30]
    assert set(' '.join(result).split())==set(words)

def test_empty_and_bad_overlap():
    assert list(chunks(''))==[]
    with pytest.raises(ValueError):
        list(chunks('x',20,20))

def test_normalization_keeps_accents():
    assert normalize('  metodología\xa0\n objetivo  ')== 'metodología objetivo'
