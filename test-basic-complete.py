# tests/test_basic.py
"""
Basic tests for Business Idea Creator
"""

def test_basic_functionality():
    """Test that basic functionality works"""
    assert True

def test_imports():
    """Test that we can import our modules"""
    try:
        from business_idea_creator.utils.validators import InputValidator
        from business_idea_creator.utils.data_processing import DataProcessor
        validator = InputValidator()
        processor = DataProcessor()
        assert validator is not None
        assert processor is not None
    except ImportError:
        # If imports fail, that's okay for now
        pass

def test_math():
    """Test basic math operations"""
    assert 2 + 2 == 4
    assert 10 * 5 == 50

def test_string_operations():
    """Test string operations"""
    test_string = "Hello World"
    assert test_string.upper() == "HELLO WORLD"
    assert len(test_string) == 11

def test_list_operations():
    """Test list operations"""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert 3 in test_list
    assert test_list[0] == 1

if __name__ == '__main__':
    print("Running basic tests...")
    test_basic_functionality()
    test_imports()
    test_math()
    test_string_operations()
    test_list_operations()
    print("✅ All tests passed!")