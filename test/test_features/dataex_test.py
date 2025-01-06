import pytest
from src.core.browser import Browser
from src.features.data_extraction import DataExtractor

class TestDataExtraction:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.browser = Browser()
        self.browser.start()
        self.extractor = DataExtractor(self.browser)
        yield
        self.browser.close()

    def test_text_extraction(self):
        self.browser.navigate_to('https://www.amazon.com/')
        heading = self.extractor.extract_text('h1')
        assert heading is not None
        assert "Example Domain" in heading

    def test_multiple_texts(self):
        self.browser.navigate_to('https://www.bbc.com/ ')
        paragraphs = self.extractor.extract_multiple_texts('p')
        assert len(paragraphs) > 0
        assert isinstance(paragraphs, list)

    def test_table_extraction(self):
        self.browser.navigate_to('https://www.w3schools.com/html/html_tables.asp')
        table_data = self.extractor.extract_table('table#customers')
        assert len(table_data) > 0
        assert isinstance(table_data, list)
        assert isinstance(table_data[0], dict)

    def test_link_extraction(self):
        self.browser.navigate_to('https://www.w3schools.com/')
        links = self.extractor.extract_links()
        assert isinstance(links, list)
        assert all('url' in link for link in links)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])