import pytest
from unittest.mock import Mock, patch
from src.features.data_extraction import DataExtractor

class TestDataExtraction:
    @pytest.fixture
    def mock_browser(self):
        with patch('src.core.browser.Browser') as mock:
            browser = Mock()
            browser.driver = Mock()
            yield browser

    @pytest.fixture
    def data_extractor(self, mock_browser):
        return DataExtractor(mock_browser)

    def test_extract_text(self, data_extractor, mock_browser):
        mock_element = Mock()
        mock_element.text = "Sample Text"
        mock_browser.find_element.return_value = mock_element

        result = data_extractor.extract_text(".sample-selector")
        assert result == "Sample Text"

    def test_extract_multiple_texts(self, data_extractor, mock_browser):
        mock_elements = [Mock(), Mock()]
        mock_elements[0].text = "Text 1"
        mock_elements[1].text = "Text 2"
        mock_browser.driver.find_elements.return_value = mock_elements

        result = data_extractor.extract_multiple_texts(".multiple-selector")
        assert result == ["Text 1", "Text 2"]

    def test_extract_table(self, data_extractor, mock_browser):
        mock_table = Mock()
        sample_html = """
        <table>
            <tr><th>Name</th><th>Age</th></tr>
            <tr><td>John</td><td>25</td></tr>
        </table>
        """
        mock_table.get_attribute.return_value = sample_html
        mock_browser.find_element.return_value = mock_table

        result = data_extractor.extract_table("table")
        assert result == [{"Name": "John", "Age": "25"}]

    @patch('requests.get')
    def test_download_images(self, mock_get, data_extractor, mock_browser, tmp_path):
        mock_images = [Mock()]
        mock_images[0].get_attribute.return_value = "http://example.com/image.jpg"
        mock_browser.driver.find_elements.return_value = mock_images

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake image data"
        mock_get.return_value = mock_response

        result = data_extractor.download_images("img", str(tmp_path))
        assert len(result) == 1
        assert result[0].endswith("image_0.jpg")

    def test_extract_links(self, data_extractor, mock_browser):
        mock_links = [Mock()]
        mock_links[0].get_attribute.return_value = "http://example.com"
        mock_links[0].text = "Example"
        mock_browser.driver.find_elements.return_value = mock_links

        result = data_extractor.extract_links("a")
        assert result == [{"url": "http://example.com", "text": "Example"}]

    def test_extract_structured_data(self, data_extractor, mock_browser):
        mock_element = Mock()
        mock_element.text = "Data"
        mock_browser.find_element.return_value = mock_element

        result = data_extractor.extract_structured_data({"key": ".selector"})
        assert result == {"key": "Data"}