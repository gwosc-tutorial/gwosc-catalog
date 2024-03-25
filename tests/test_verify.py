from verify import verify_upload_schema

def test_global_keys():
    bad_keys = {"a": 1, "b": 2}
    is_correct = verify_upload_schema(bad_keys)
    assert is_correct == True
